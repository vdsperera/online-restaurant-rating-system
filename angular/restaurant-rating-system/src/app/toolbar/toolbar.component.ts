import { Component, OnInit } from '@angular/core';
import { MenuItem } from '../menu-item';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent implements OnInit {
  
  menuItems: MenuItem[] = [
    {
      label: 'Blog',
      icon: 'rss_feed',
      showOnMobile: false,
      showOnTablet: false,
      showOnDesktop: false,
      route: ''
    },
    {
      label: 'Showcase',
      icon: 'slideshow',
      showOnMobile: false,
      showOnTablet: false,
      showOnDesktop: true,
      route: ''
    },
    {
      label: 'Docs',
      icon: 'notes',
      showOnMobile: false,
      showOnTablet: true,
      showOnDesktop: true,
      route: ''
    },
    {
      label: 'Add Restaurant',
      icon: 'add_circle',
      showOnMobile: false,
      showOnTablet: false,
      showOnDesktop: true,
      route: '/registerrestaurant'
    },
    {
      label: 'About',
      icon: 'help',
      showOnMobile: false,
      showOnTablet: true,
      showOnDesktop: true,
      route: ''
    },
    {
      label: 'Sign Up',
      icon: 'login',
      showOnMobile: true,
      showOnTablet: true,
      showOnDesktop: true,
      route: ''
    },


  
  ];

  constructor() { }

  ngOnInit(): void {
  }

}
