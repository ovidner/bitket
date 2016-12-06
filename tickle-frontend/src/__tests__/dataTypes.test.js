import { Money, sumMoney } from '../dataTypes'

describe('Money', () => {
  it('employs 2 decimal places', () => {
    expect(Money('1.00').div(3).toFixed()).toEqual('0.33')
  })

  describe('normalize', () => {
    it('returns a Money instance rounded to two decimals', () => {
      expect(Money('-0').normalize().eq(0)).toBe(true)
      expect(Money('-0.0045').normalize().eq(0)).toBe(true)
      expect(Money('-0.045').normalize().eq(-0.05)).toBe(true)
      expect(Money('-0.45').normalize().eq(-0.45)).toBe(true)
      expect(Money('-4.5').normalize().eq(-4.5)).toBe(true)
      expect(Money('-45').normalize().eq(-45)).toBe(true)
      expect(Money('0').normalize().eq(0)).toBe(true)
      expect(Money('0.0045').normalize().eq(0)).toBe(true)
      expect(Money('0.045').normalize().eq(0.05)).toBe(true)
      expect(Money('0.45').normalize().eq(0.45)).toBe(true)
      expect(Money('4.5').normalize().eq(4.5)).toBe(true)
      expect(Money('45').normalize().eq(45)).toBe(true)
    })
  })

  describe('toRepr', () => {
    it('returns a string representation with two decimals', () => {
      expect(Money('-0').toRepr()).toEqual('0.00')
      expect(Money('-0.0045').toRepr()).toEqual('0.00')
      expect(Money('-0.045').toRepr()).toEqual('-0.05')
      expect(Money('-0.45').toRepr()).toEqual('-0.45')
      expect(Money('-4.5').toRepr()).toEqual('-4.50')
      expect(Money('-45').toRepr()).toEqual('-45.00')
      expect(Money('0').toRepr()).toEqual('0.00')
      expect(Money('0.0045').toRepr()).toEqual('0.00')
      expect(Money('0.045').toRepr()).toEqual('0.05')
      expect(Money('0.45').toRepr()).toEqual('0.45')
      expect(Money('4.5').toRepr()).toEqual('4.50')
      expect(Money('45').toRepr()).toEqual('45.00')
    })
  })
})

describe('sumMoney', () => {
  it('takes numbers, string representations of numbers and Money objects as arguments and returns the sum of them as a Money object', () => {
    expect(sumMoney(
      2, 2.5, -1, -1.05,
      '2', '2.5', '-1', '-1.05',
      Money('2'), Money('2.5'), Money('-1'), Money('-1.05'))
    ).toEqual(Money('7.35'))
  })
})
