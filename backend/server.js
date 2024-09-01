const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv').config();
const routes = require("./routes/routes")

const app = express();

app.use(cors());
app.use(express.json());
app.use('/', routes);

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

//for testing
app.get('/', (req, res) => {
  res.send('Hello from MERN Auth API');
});