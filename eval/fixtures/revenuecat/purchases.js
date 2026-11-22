import Purchases from 'react-native-purchases';

export const ANNUAL_PRODUCT_ID = 'com.habitly.pro.annual';

export async function getCustomerInfo() {
  return Purchases.getCustomerInfo();
}

// TODO: isPro(customerInfo) should return true when the user has paid for Pro.
