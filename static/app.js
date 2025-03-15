let username = "";

function registerUser() {
    username = document.getElementById("username").value;
    if (!username) {
        alert("Please enter your name");
        return;
    }
    fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: username })
    }).then(() => {
        document.querySelector(".user-input").style.display = "none";
        document.querySelector(".game-container").style.display = "block";
        document.getElementById("welcome").innerText = `Welcome, ${username}!`;
        loadLeaderboard();
    });
}

function playGame(playerChoice) {
    const choices = ["rock", "paper", "scissors"];
    const computerChoice = choices[Math.floor(Math.random() * 3)];
    let result = "";

    if (playerChoice === computerChoice) {
        result = "It's a tie!";
    } else if (
        (playerChoice === "rock" && computerChoice === "scissors") ||
        (playerChoice === "paper" && computerChoice === "rock") ||
        (playerChoice === "scissors" && computerChoice === "paper")
    ) {
        result = "You win!";
        updateScore(1);
    } else {
        result = "You lose!";
    }

    document.getElementById("result").innerText = `You chose ${playerChoice}, computer chose ${computerChoice}. ${result}`;
}

function updateScore(points) {
    fetch('/update_score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: username, score: points })
    }).then(() => {
        loadLeaderboard();
    });
}

function loadLeaderboard() {
    fetch('/leaderboard')
        .then(response => response.json())
        .then(data => {
            let leaderboard = document.getElementById("leaderboard-list");
            leaderboard.innerHTML = "";
            data.forEach(entry => {
                leaderboard.innerHTML += `<li>${entry[0]} - ${entry[1]} points</li>`;
            });
        });
}
