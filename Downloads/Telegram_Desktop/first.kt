package com.example.lazyrow

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.annotation.DrawableRes
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.outlined.AccountCircle
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.lazyrow.ui.theme.LazyRowTheme
import androidx.compose.runtime.setValue
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController


import com.google.accompanist.pager.*

data class MovieItem(
    val title: String,
    val zhanr: String,
    val rating: String,
    @DrawableRes val image: Int
)

class MainActivity : ComponentActivity() {
    companion object {
        val items: List<MovieItem> = listOf(
            MovieItem(
                title = "Близкие",
                zhanr = "Драма",
                rating = "10",
                image = R.drawable.img
            ),
            MovieItem(
                title = "Близкие",
                zhanr = "Драма",
                rating = "10",
                image = R.drawable.img
            ),
            MovieItem(
                title = "Близкие",
                zhanr = "Драма",
                rating = "10",
                image = R.drawable.img
            ),
            MovieItem(
                title = "Близкие",
                zhanr = "Драма",
                rating = "10",
                image = R.drawable.img
            ),
            MovieItem(
                title = "Близкие",
                zhanr = "Драма",
                rating = "10",
                image = R.drawable.img
            ),
            MovieItem(
                title = "Близкие",
                zhanr = "Драма",
                rating = "10",
                image = R.drawable.img
            ),
            MovieItem(
                title = "Близкие",
                zhanr = "Драма",
                rating = "10",
                image = R.drawable.img
            ),
        )
    }

    //Home Screen
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            LazyRowTheme() {
                MyApp()
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(16.dp)
                    ) {
                        Text(
                            text = "Skillcinema",
                            style = MaterialTheme.typography.headlineMedium,
                            modifier = Modifier.padding(bottom = 12.dp).padding(top = 30.dp)
                        )

                        Spacer(modifier = Modifier.padding(8.dp))
                        SectionTitle(title = "Премьеры")
                        LazyRowScreen()

                        Spacer(modifier = Modifier.height(2.dp))

                        SectionTitle(title = "Популярное")
                        LazyRowScreen()

                        Spacer(modifier = Modifier.height(2.dp))

                        SectionTitle(title = "Боевики США")
                        LazyRowScreen()
                    }
                }
                var selectedIndex by androidx.compose.runtime.remember {
                    mutableIntStateOf(0)
                }
                Scaffold(
                    bottomBar = {
                        NavigationBar {
                            bottomNavItems.forEachIndexed { index, bottomNavItem ->
                                NavigationBarItem(
                                    selected = index == selectedIndex,
                                    onClick = { selectedIndex = index },
                                    icon = {
                                        Icon(
                                        imageVector = if (index == selectedIndex) {
                                            bottomNavItem.selectedIcon
                                        } else {
                                            bottomNavItem.unselectedIcon
                                        }, contentDescription = bottomNavItem.title
                                    )
                                }, label = {
                                    androidx.compose.material3.Text(text = bottomNavItem.title)
                                }
                            )
                        }
                    }
                }
            ) { paddingValues ->
                androidx.compose.foundation.layout.Column(
                    modifier = androidx.compose.ui.Modifier
                        .fillMaxSize()
                        .padding(paddingValues),
                    verticalArrangement = androidx.compose.foundation.layout.Arrangement.Center,
                    horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally
                ) {
                    when (selectedIndex) {
                        0 -> com.example.lazyrow.bottombar.HomeScreen()
                        1 -> com.example.lazyrow.bottombar.SearchScreen()
                        2 -> com.example.lazyrow.bottombar.ProfileScreen()
                    }
                }
            }
        }
    }
}
val bottomNavItems = kotlin.collections.listOf(
    com.example.lazyrow.bottombar.BottomNavItem(
        title = "Home",
        route = "home",
        selectedIcon = androidx.compose.material.icons.Icons.Filled.Home,
        unselectedIcon = androidx.compose.material.icons.Icons.Outlined.Home
    ),
    com.example.lazyrow.bottombar.BottomNavItem(
        title = "Search",
        route = "search",
        selectedIcon = androidx.compose.material.icons.Icons.Filled.Search,
        unselectedIcon = androidx.compose.material.icons.Icons.Outlined.Search
    ),
    com.example.lazyrow.bottombar.BottomNavItem(
        title = "Profile",
        route = "profile",
        selectedIcon = androidx.compose.material.icons.Icons.Filled.AccountCircle,
        unselectedIcon = androidx.compose.material.icons.Icons.Outlined.AccountCircle
    )

)

@Composable
fun MyApp() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "onboarding") {
        composable("onboarding") {
            OnboardingScreen(navController = navController)
        }
        composable("main") {
            MainScreen()
        }
    }
}

// Data class for OnboardingPage
data class OnboardingPage(val image: Int, val title: String)
@Suppress("DEPRECATION")
@OptIn(ExperimentalPagerApi::class)
@Composable
fun OnboardingScreen(navController: NavController) {
    val onboardingPages = listOf(
        OnboardingPage(
            image = R.drawable.share,
            title = "Узнавай о премьерах"
        ),
        OnboardingPage(
            image = R.drawable.share,
            title = "Создавай коллекции"
        ),
        OnboardingPage(
            image = R.drawable.share,
            title = "Делись с друзьями"
        )
    )

    val pagerState = rememberPagerState()
    val scope = rememberCoroutineScope()

    Box(modifier = Modifier.fillMaxSize()) {
        // Fixed Skillcinema text outside the HorizontalPager
        Column {
            // "Skillcinema" title stays at the top left
            Text(
                text = "Skillcinema",
                fontSize = 24.sp,
                modifier = Modifier
                    .padding(start = 25.dp, top = 30.dp)
                    .align(Alignment.Start)
            )

            Spacer(modifier = Modifier.height(16.dp))

            // HorizontalPager for swiping between pages
            HorizontalPager(
                state = pagerState,
                count = onboardingPages.size,
                modifier = Modifier.fillMaxSize()
            ) { page ->
                OnboardingPageContent(onboardingPages[page], pagerState.currentPage)
            }
        }

        // "Пропустить" button at the top right (outside of the pager)
        Text(
            text = "Пропустить",
            fontSize = 19.sp,
            color = Color.LightGray,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(top = 35.dp, end = 16.dp)
                .clickable {
                    navController.navigate("main")  // Skip to main page
                }
        )

        // Fixed Dots at the bottom left
        Row(
            modifier = Modifier
                .align(Alignment.BottomStart)  // Keep dots in the bottom left corner
                .padding(start = 20.dp, bottom = 100.dp),
            horizontalArrangement = Arrangement.Start
        ) {
            repeat(onboardingPages.size) { index ->
                val color = if (index == pagerState.currentPage) Color.Black else Color.Gray
                Box(
                    modifier = Modifier
                        .padding(2.dp)  // Small padding between dots
                        .size(8.dp)
                        .clip(CircleShape)
                        .background(color)
                )
            }
        }
    }
}

@Composable
fun OnboardingPageContent(page: OnboardingPage, currentPage: Int) {
    // Split the title into the first word and the remaining part
    val titleParts = page.title.split(" ", limit = 2)
    val firstWord = titleParts.getOrElse(0) { "" }
    val remainingWords = titleParts.getOrElse(1) { "" }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(start = 16.dp, bottom = 50.dp),  // Adjust bottom padding
        verticalArrangement = Arrangement.Center,  // Center the content vertically
        horizontalAlignment = Alignment.Start  // Align content to the left for title
    ) {
        // Main Image (centered horizontally)
        Image(
            painter = painterResource(id = page.image),
            contentDescription = null,
            contentScale = ContentScale.Fit,
            modifier = Modifier
                .fillMaxWidth(0.7f)
                .width(350.dp)
                .height(300.dp)
                .align(Alignment.CenterHorizontally)  // Center the image
        )

        Spacer(modifier = Modifier.height(30.dp))  // Space between the image and title

        // Page title with the first word on the first line and remaining words on the second line
        Column(
            modifier = Modifier.align(Alignment.Start)
        ) {
            // First word on the first line
            Text(
                text = firstWord,
                fontSize = 35.sp,
                lineHeight = 40.sp,
                modifier = Modifier.fillMaxWidth()
            )

            // Remaining words on the second line
            Text(
                text = remainingWords,
                fontSize = 35.sp,
                lineHeight = 40.sp,
                modifier = Modifier.fillMaxWidth()
            )
        }

        Spacer(modifier = Modifier.height(35.dp))  // Space between title and bottom of the screen
    }
}



// Example MainScreen (after onboarding)
@Composable
fun MainScreen() {
    Box(
        modifier = Modifier
            .fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text(text = "Welcome to the Main Screen!", fontSize = 24.sp)
    }
}




