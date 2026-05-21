import { Component, inject, Input, signal } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { InferenceService } from '../../../services/InferenceService.service';

@Component({
  selector: 'app-prediction-result',
  imports: [],
  templateUrl: './prediction-result.html',
  styleUrl: './prediction-result.css',
})
export class PredictionResult {
  @Input() inputImage?: ImageData;

  private inferenceService = inject(InferenceService);
  private toastrService = inject(ToastrService);

  protected loadingResults = signal(false);
  protected results = signal<[string, number][]>([]);

  protected onStartInference() {
    if (!this.inputImage) {
      this.toastrService.error('Please upload image first.', 'No image uploaded.');
      return;
    }

    this.loadingResults.set(true);
    this.inferenceService.runInference(this.inputImage, 224, 224).subscribe({
      next: (value) => {
        this.results.set(value);
        this.loadingResults.set(false);
      },
      error: (err) => this.toastrService.error(err, 'Failed to load labels.'),
    });
  }

  protected loadLabels() {}

  private setLabels(results: string[]) {}
}
