import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-custom-dropdown',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './custom-dropdown.component.html',
  styleUrls: ['./custom-dropdown.component.css'],
})
export class CustomDropdownComponent {
  searchText: string = '';
  selectedRow: any = null;
  showDropdown: boolean = false;

  options = [
    { id: 1, name: 'Alice', email: 'alice@example.com', role: 'Admin', location: 'New York' },
    { id: 2, name: 'Bob', email: 'bob@example.com', role: 'User', location: 'California' },
    { id: 3, name: 'Charlie', email: 'charlie@example.com', role: 'Editor', location: 'Texas' },
    { id: 4, name: 'David', email: 'david@example.com', role: 'User', location: 'Florida' },
    { id: 5, name: 'Eva', email: 'eva@example.com', role: 'Admin', location: 'Ohio' },
  ];

  get filteredOptions() {
    if (!this.searchText) {
      return this.options;
    }
    const lower = this.searchText.toLowerCase();
    return this.options.filter(opt =>
      Object.values(opt).some(val =>
        val.toString().toLowerCase().includes(lower)
      )
    );
  }

  filterOptions() {
    this.showDropdown = true;
  }

  highlight(text: string): string {
    if (!this.searchText) return text;
    const re = new RegExp(`(${this.searchText})`, 'gi');
    return text.replace(re, `<mark>$1</mark>`);
  }

  selectRow(row: any) {
    this.selectedRow = row;
    this.searchText = `${row.name} (${row.email})`;
    this.showDropdown = false;
  }

  onBlur() {
    setTimeout(() => {
      this.showDropdown = false;
    }, 200); // Delay to allow row click
  }
}
