package com.example.lazyrow

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun LazyRowScreen(){
    LazyRow (
        modifier = Modifier.fillMaxWidth(),
        contentPadding = PaddingValues(1.dp)
    ){
        itemsIndexed(MainActivity.items){ index, item ->
            RowItem(item = item)
            Spacer(modifier = Modifier.width(1.dp))
        }
    }
}

@Composable
fun RowItem(item: MovieItem) {
    MovieCard(item = item)
}

@Composable
fun MovieCard(item: MovieItem) {
    Card(
        modifier = Modifier
            .width(80.dp)
            .padding(8.dp)
    ) {
        Column(
            modifier = Modifier.background(Color.White)
        ) {
            Box(
                modifier = Modifier
                    .height(100.dp)
                    .fillMaxWidth()
                    .background(Color.Gray)
            ) {
                Image(
                    modifier = Modifier.fillMaxSize(),
                    painter = painterResource(id = item.image),
                    contentDescription = item.title
                )
                Text(
                    text = item.rating,
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(10.dp)
                        .background(Color(0xFF6600ff),CircleShape),
                    fontSize = 12.sp,
                    color = Color.White
                )
            }
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = item.title,
                modifier = Modifier.padding(horizontal = 2.dp).height(17.dp),
                fontWeight = FontWeight.SemiBold,
                fontSize = 13.sp
            )
            Text(
                text = item.zhanr,
                modifier = Modifier.padding(horizontal = 2.dp),
                fontWeight = FontWeight.Bold,
                fontSize = 10.sp
            )
        }
    }
}

@Composable
fun SectionTitle(title: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.labelLarge.copy(fontWeight = FontWeight.Bold)
        )
        Text(
            text = "Все",
            style = MaterialTheme.typography.labelSmall.copy(color = Color.Blue), // Customize the "Все" text style
            modifier = Modifier.clickable {
                // Handle "Все" click action here
            }
        )
    }
}
