const { CATALOG } = require('./catalog');

// Order lines look like { id: 'line_9', sku: 'SKU-002', qty: 2 }
function computeTotal(order) {
  let total = 0;
  for (const line of order.lines) {
    const product = CATALOG[line.id];
    total += product.price * line.qty;
  }
  return Math.round(total * 100) / 100;
}

module.exports = { computeTotal };
