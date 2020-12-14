export class DishRating
{
  private dish_name: string;
  private dish_id: number;
  private no_of_ratings: number;
  private rating: number;

  // constructor(name: string, address: string, phone_number: string, longitude: string, latitude: string)
  // {
  //   this.name = name;
  //   this.address = address;
  //   this.phone_number = phone_number;
  //   this.longitude = longitude;
  //   this.latitude = latitude;  
  // }

  public set_dish_name(dish_name: string)
  {
    this.dish_name = dish_name;
  }

  public set_dish_id(dish_id: number)
  {
    this.dish_id = dish_id;
  }

  public set_no_of_ratings(no_of_ratings: number)
  {
    this.no_of_ratings = no_of_ratings;
  }

  public set_rating(rating: number)
  {
    this.rating = rating;
  }

  public get_ratings()
  {
    let model = {
      "dish_id":this.dish_id,
      "dish_name":this.dish_name,
      "rating": this.rating
    }
    return model
  }  
}