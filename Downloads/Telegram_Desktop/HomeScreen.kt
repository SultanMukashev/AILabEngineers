package com.example.lazyrow.bottombar

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Modifier

@androidx.compose.runtime.Composable
fun HomeScreen() {
    androidx.compose.foundation.layout.Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Skillcinema",
            style = androidx.compose.material3.MaterialTheme.typography.headlineMedium,
            modifier = androidx.compose.ui.Modifier.padding(bottom = 16.dp).padding(top = 50.dp)
        )

        androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.padding(12.dp))
        com.example.lazyrow.SectionTitle(title = "Премьеры")
        com.example.lazyrow.LazyRowScreen()

        androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.height(2.dp))

        com.example.lazyrow.SectionTitle(title = "Популярное")
        com.example.lazyrow.LazyRowScreen()

        androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.height(2.dp))

        com.example.lazyrow.SectionTitle(title = "Боевики США")
        com.example.lazyrow.LazyRowScreen()
    }
}