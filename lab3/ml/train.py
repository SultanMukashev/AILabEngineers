import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix

load_dotenv()


def process_age(df, cut_points, label_names):
    df["age"] = df["age"].fillna(-0.5)
    df["age_categories"] = pd.cut(df["age"], cut_points, labels=label_names)
    return df


def create_dummies(df, column_name):
    dummies = pd.get_dummies(df[column_name], prefix=column_name)
    return pd.concat([df, dummies], axis=1)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('POSTGRES_PORT')
    )


def load_data(conn):
    test = pd.read_sql("SELECT * FROM test;", conn)
    train = pd.read_sql("SELECT * FROM train;", conn)
    return train, test


def prepare_model(train, test):
    cut_points = [-1, 0, 5, 12, 18, 35, 60, 100]
    label_names = ["Missing", 'Infant', 'Child', 'Teenager', 'Young Adult', 'Adult', 'Senior']

    train = process_age(train, cut_points, label_names)
    test = process_age(test, cut_points, label_names)

    for col in ["sex", "age_categories", "pclass"]:
        train = create_dummies(train, col)
        test = create_dummies(test, col)

    columns = ['pclass_1', 'pclass_2', 'pclass_3', 'sex_female', 'sex_male',
               'age_categories_Missing', 'age_categories_Infant',
               'age_categories_Child', 'age_categories_Teenager',
               'age_categories_Young Adult', 'age_categories_Adult',
               'age_categories_Senior']

    lr = LogisticRegression()
    all_X = train[columns]
    all_y = train['survived']

    train_X, test_X, train_y, test_y = train_test_split(all_X, all_y, test_size=0.2, random_state=0)
    lr.fit(train_X, train_y)
    predictions = lr.predict(test_X)
    print(f"Model Accuracy: {accuracy_score(test_y, predictions):.2f}")

    lr.fit(all_X, all_y)
    return lr, columns, test


def predict_survival(model, columns, passenger_data):
    passenger_df = pd.DataFrame([passenger_data])

    cut_points = [-1, 0, 5, 12, 18, 35, 60, 100]
    label_names = ["Missing", 'Infant', 'Child', 'Teenager', 'Young Adult', 'Adult', 'Senior']
    passenger_df = process_age(passenger_df, cut_points, label_names)

    for col in ["sex", "age_categories", "pclass"]:
        passenger_df = create_dummies(passenger_df, col)

    for col in columns:
        if col not in passenger_df:
            passenger_df[col] = 0

    prediction = model.predict(passenger_df[columns])
    return "survived" if prediction[0] == 1 else "did not survive"


def main():
    # Load data and model once at startup
    conn = get_db_connection()
    train, test = load_data(conn)
    conn.close()
    model, columns, test_data = prepare_model(train, test)

    while True:
        print("\nTitanic Survival Predictor")
        print("1. Use test data")
        print("2. Enter passenger details")
        print("3. exit")

        choice = input("\nEnter your choice (1/2/3): ").lower()

        if choice == "3":
            print("Exiting the program...")
            break

        if choice == "1":
            predictions = model.predict(test_data[columns])
            test_data['predicted_survival'] = ["survived" if x == 1 else "did not survive" for x in predictions]
            print(test_data[['passengerid', 'pclass', 'sex', 'age', 'predicted_survival']].head(10))
        elif choice == "2":
            print("\nEnter passenger details:")
            try:
                pclass = int(input("Passenger class (1, 2, or 3): "))
                sex = input("Sex (male/female): ")
                age = float(input("Age: "))

                passenger = {
                    'pclass': pclass,
                    'sex': sex.lower(),
                    'age': age
                }

                result = predict_survival(model, columns, passenger)
                print(f"\nPrediction: This passenger would have {result}")
            except ValueError:
                print("Invalid input. Please enter valid values.")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()