import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-data-bar',
  imports: [],
  templateUrl: './data-bar.html',
  styleUrl: './data-bar.css',
})
export class DataBar {
  @Input({ required: true }) public value!: number;
  @Input({ required: true }) public totalValue!: number;

  @Input() public maxWidth = 100;
}
