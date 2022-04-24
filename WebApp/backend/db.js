const Pool = require('pg').Pool
const configObj = require('./config')

const pool = new Pool(configObj)

module.exports = pool

