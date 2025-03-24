const express = require("express");
const { exec } = require("child_process");

const app = express();
const PORT = 3000;

app.get("/fetch-articles", (req, res) => {
    exec("python scraper.py", (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ error: "Failed to fetch webpage" });
        }
        try {
            const data = JSON.parse(stdout); // Parse Python output
            res.json(data);
        } catch (err) {
            res.status(500).json({ error: "Failed to parse Python response" });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});




