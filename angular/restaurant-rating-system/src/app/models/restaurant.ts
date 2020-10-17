export class Restaurant
{
  private name: string;
  private address: string
  private phone_number: string
  private longitude: string
  private latitude: string  

  constructor(name: string, address: string, phone_number: string, longitude: string, latitude: string)
  {
    this.name = name;
    this.address = address;
    this.phone_number = phone_number;
    this.longitude = longitude;
    this.latitude = latitude;  
  }
}