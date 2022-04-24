const dotenv = require('dotenv')
dotenv.config({path: __dirname + '/.env'})

const {
  DB_HOST,
  DB_USER,
  DB_PASSWORD,
  DB_PORT,
  DB_NAME,
} = process.env

const configObj = {
  host: DB_HOST,
  database: DB_NAME,
  user: DB_USER,
  password: DB_PASSWORD,
  port: DB_PORT
}

module.exports = configObj
