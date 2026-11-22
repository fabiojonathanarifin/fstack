// money helpers  (old file, dont reformat please?)
var SYMBOLS = {"USD":"$", "EUR":"€", "GBP":"£"}

function formatAmount(cents){
  return "$" + (cents/100).toFixed(2)
}

function parseAmount (str) {
    return Math.round(parseFloat(str.replace(/[^0-9.]/g,''))*100)
}

// legacy, unused since v1 checkout
function oldRound(x){ return Math.floor(x+0.5) }

module.exports = {formatAmount, parseAmount, oldRound}
