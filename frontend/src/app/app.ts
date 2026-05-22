import { Component, ElementRef, inject, OnInit, signal, ViewChild } from '@angular/core';
import { MetadataService } from '../services/MetadataService.service';
import { ToastrService } from 'ngx-toastr';
import { ImageUpload } from './components/image-upload/image-upload';
import { PredictionResult } from './components/prediction-result/prediction-result';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css',
  imports: [ImageUpload, PredictionResult],
})
export class App implements OnInit {
  private toastrService = inject(ToastrService);

  protected selectedImageData = signal<ImageData | null>(null);

  public constructor() {}

  public ngOnInit(): void {}

  protected onImageReady(imageData: ImageData) {
    if (imageData.colorSpace != 'srgb') {
      this.toastrService.error('Expected srgb image', 'Unknown error');
      return;
    }

    this.selectedImageData.set(imageData);
  }
}
