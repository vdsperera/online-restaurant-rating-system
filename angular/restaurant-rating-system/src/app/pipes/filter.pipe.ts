import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'appFilter'})
export class FilterPipe implements PipeTransform
{
  transform(items: any[], search_text: string): any[]
  {
  	if(!items) return [];
  	if(!search_text) return items;

  	search_text = search_text.toLocaleLowerCase()

  	return items.filter((it) => {
  		console.log(it.restaurant_name)
  		return it.address.toLocaleLowerCase().includes(search_text)
  	})
  }


}