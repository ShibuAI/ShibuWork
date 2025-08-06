import { Component, signal } from '@angular/core';
import { MainLayoutComponent } from './components/main-layout/main-layout.component';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MainLayoutComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  currentView = signal('home');

  showFileProcess() {
    this.currentView.set('fileProcess');
  }

  showHome() {
    this.currentView.set('home');
  }
}