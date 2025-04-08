#include <aws/core/Aws.h>
#include <aws/core/auth/AWSCredentialsProvider.h> // Required for credentials providers
#include <aws/s3/S3Client.h>
#include <aws/s3/model/PutObjectRequest.h>
#include <aws/s3/model/CreateBucketRequest.h>
#include <fstream>
#include <iostream>

int main() {
    // Preparing AWS SDK options
    Aws::SDKOptions options;
    Aws::InitAPI(options);
    {
        // Set up credentials using static values
        auto credentialsProvider = Aws::MakeShared<Aws::Auth::SimpleAWSCredentialsProvider>(
            "CustomAllocationTag",
            "minioadmin", 
            "minioadmin123"
        );

        // Configure client settings for MinIO
        Aws::Client::ClientConfiguration config;
        config.endpointOverride = "http://localhost:9000";
        config.scheme = Aws::Http::Scheme::HTTP;
        config.region = "us-east-1";
        config.verifySSL = false;

        // Create S3 client with credentials and configuration
        Aws::S3::S3Client s3_client(
            credentialsProvider,
            config,
            Aws::Client::AWSAuthV4Signer::PayloadSigningPolicy::Never,
            false // Use path-style addressing
        );

        Aws::S3::Model::CreateBucketRequest createBucketRequest;
        createBucketRequest.SetBucket("test-bucket");

        auto createBucketOutcome = s3_client.CreateBucket(createBucketRequest);

        if (createBucketOutcome.IsSuccess()) {
            std::cout << "Bucket 'test-bucket' created successfully." << std::endl;
        } else {
            const auto& err = createBucketOutcome.GetError();
            if (err.GetExceptionName() == "BucketAlreadyOwnedByYou") {
                std::cout << "Bucket already exists." << std::endl;
            } else {
                std::cerr << "Failed to create bucket: " << err.GetMessage() << std::endl;
            }
        }

        // Create and configure the PutObject request
        Aws::S3::Model::PutObjectRequest request;
        request.SetBucket("test-bucket");
        request.SetKey("orders.csv");

        std::shared_ptr<Aws::IOStream> inputData =
        Aws::MakeShared<Aws::FStream>("FileAllocationTag", "../data/orders.csv", std::ios_base::in | std::ios_base::binary);
        request.SetBody(inputData);

        // Perform the upload
        auto outcome = s3_client.PutObject(request);
        if (outcome.IsSuccess()) {
            std::cout << "Upload successful!" << std::endl;
        } else {
            std::cerr << "Upload error: " << outcome.GetError().GetMessage() << std::endl;
        }
    }
    Aws::ShutdownAPI(options); // Closing the connection

    return 0;
}