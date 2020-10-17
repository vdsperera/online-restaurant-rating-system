export class Rating
{
  private dish_rating: number;
  private price_rating: number;
  private service_rating: number; 

  // constructor(name: string, address: string, phone_number: string, longitude: string, latitude: string)
  // {
  //   this.name = name;
  //   this.address = address;
  //   this.phone_number = phone_number;
  //   this.longitude = longitude;
  //   this.latitude = latitude;  
  // }

  public set_dish_rating(dish_rating: number)
  {
    this.dish_rating = dish_rating;
  }

  public set_price_rating(price_rating: number)
  {
    this.price_rating = price_rating;
  }

  public set_service_rating(service_rating: number)
  {
    this.service_rating = service_rating;
  }  
}