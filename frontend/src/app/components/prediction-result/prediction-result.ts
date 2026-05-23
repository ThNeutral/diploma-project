import { Component, computed, inject, Input, OnInit, signal } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { InferenceService } from '../../../services/InferenceService.service';
import { DataBar } from '../data-bar/data-bar';
import { MetadataService } from '../../../services/MetadataService.service';

@Component({
  selector: 'app-prediction-result',
  imports: [DataBar],
  templateUrl: './prediction-result.html',
  styleUrl: './prediction-result.css',
})
export class PredictionResult implements OnInit {
  @Input() inputImage: ImageData | null = null;

  private inferenceService = inject(InferenceService);
  private metadataService = inject(MetadataService);
  private toastrService = inject(ToastrService);

  protected loadingResults = signal(false);
  protected results = signal<[number, number][]>([]);

  protected loadingLabels = signal(false);
  protected labels = signal<string[]>([]);

  protected sortedResults = computed<[string, number, number][]>(() => {
    const total = this.results().reduce((acc, x) => acc + x[1], 0);
    const labels = this.labels();

    return this.results()
      .sort((a, b) => {
        if (a[1] > b[1]) return -1;
        if (a[1] < b[1]) return 1;
        return 0;
      })
      .map((x) => [labels[x[0]], x[1], total]);
  });

  public ngOnInit(): void {
    this.loadLabels();
  }

  private loadLabels() {
    this.loadingLabels.set(true);
    this.metadataService.getLabels().subscribe({
      next: (value) => {
        this.labels.set([...value]);
        this.loadingLabels.set(false);
      },
      error: (err) => {
        const message = err?.error?.message ?? err?.message ?? err;
        this.toastrService.error(message, 'Failed to load labels.');
        this.loadingResults.set(false);
      },
    });
  }

  protected onStartInference(event: Event) {
    event.preventDefault();

    if (!this.inputImage) {
      this.toastrService.error('Please upload image first.', 'No image uploaded.');
      return;
    }

    this.loadingResults.set(true);
    this.inferenceService
      .runInference(this.inputImage, this.inputImage.width, this.inputImage.height)
      .subscribe({
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
