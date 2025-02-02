const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
const PORT = 5000;
const DISCORD_API_BASE = "https://discord.com/api/v10";
const HEADERS = {
    Authorization: "Bot MTMzNTA0MzI3Nzg4MzE3OTExMQ.GmsOs6.2FAB70nmUv7YJdx_jPdDpq0O4kUpK4lTX0dSR4"
};

app.use(cors()); // Permitir requisições do frontend

const getUserData = async (userId) => {
    try {
        const url = `${DISCORD_API_BASE}/users/${userId}`;
        const response = await axios.get(url, { headers: HEADERS });
        const user = response.data;

        const avatarUrl = user.avatar
            ? `https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.${user.avatar.startsWith("a_") ? "gif" : "png"}?size=512`
            : "https://cdn.discordapp.com/embed/avatars/1.png";

        return {
            id: user.id,
            username: user.username,
            display_name: user.global_name || user.username,
            avatar: avatarUrl
        };
    } catch (error) {
        return null;
    }
};

app.get("/user/:userId", async (req, res) => {
    const userData = await getUserData(req.params.userId);
    if (userData) {
        res.json(userData);
    } else {
        res.status(404).json({ error: "User not found" });
    }
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on port ${PORT}`);
});
