const user = await getAuthenticated();

if (!user || (user.id != 57)) {
    document.getElementById("lotteryBanner").style.display = 'none';
}
