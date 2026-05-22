import { Component, computed, inject, Input, signal } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { InferenceService } from '../../../services/InferenceService.service';

@Component({
  selector: 'app-prediction-result',
  imports: [],
  templateUrl: './prediction-result.html',
  styleUrl: './prediction-result.css',
})
export class PredictionResult {
  @Input() inputImage: ImageData | null = null;

  private inferenceService = inject(InferenceService);
  private toastrService = inject(ToastrService);

  protected loadingResults = signal(false);
  protected results = signal<[string, number][]>([]);

  protected sortedResults = computed<[string, number, number][]>(() => {
    const total = this.results().reduce((acc, x) => acc + x[1], 0);

    return this.results()
      .sort((a, b) => {
        if (a[1] > b[1]) return -1;
        if (a[1] < b[1]) return 1;
        return 0;
      })
      .map((x) => [x[0], x[1], total]);
  });

  protected onStartInference(event: Event) {
    event.preventDefault();

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
      error: (err) => {
        const message = err?.error?.message ?? err?.message ?? err;
        this.toastrService.error(message, 'Failed to run inference.');
        this.loadingResults.set(false);
      },
    });
  }
}
