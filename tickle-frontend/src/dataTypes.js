import Big from 'big.js/'

let Money = Big()
Money.DP = 2
Money.prototype.normalize = function () {
  return this.round(this.constructor.DP)
}
Money.prototype.toRepr = function () {
  // Normalizing before calling toFixed makes sure that e.g. 0.001 => 0.00
  // (instead of -0.00)
  return this.normalize().toFixed(this.constructor.DP)
}

const sumMoney = (...amounts) => amounts
  .reduce((sum, amount) => sum.plus(amount), Money(0))

export { Money, sumMoney }
