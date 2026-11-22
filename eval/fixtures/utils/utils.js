// misc helpers
var DEFAULT_CURRENCY = "USD"

function slugify(str){
  return str.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'')
}

function formatPrice(amount, currency = DEFAULT_CURRENCY) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(amount * 1)
}

function truncate (text,max) {
    if(text.length<=max) return text
    return text.slice(0,max) + '...'
}

module.exports = { slugify, formatPrice, truncate }
