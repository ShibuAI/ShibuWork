import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CustomDropdownComponent } from './custom-dropdown/custom-dropdown.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    CustomDropdownComponent
  ],
  template: `
    <h1>Custom Dropdown Example</h1>
    <app-custom-dropdown></app-custom-dropdown>
  `,
})
export class AppComponent {}
