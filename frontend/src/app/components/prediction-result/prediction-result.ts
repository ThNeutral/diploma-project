import { Component, computed, inject, Input, OnInit, signal } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { InferenceService } from '../../../services/InferenceService.service';
import { DataBar } from '../data-bar/data-bar';
import { MetadataService } from '../../../services/MetadataService.service';
import { BreakpointObserver } from '@angular/cdk/layout';
import { MobileObserver } from '../../../services/MobileObserver.service';

@Component({
  selector: 'app-prediction-result',
  imports: [DataBar],
  templateUrl: './prediction-result.html',
  styleUrl: './prediction-result.css',
})
export class PredictionResult implements OnInit {
  @Input() inputImage: Blob | null = null;

  private inferenceService = inject(InferenceService);
  private metadataService = inject(MetadataService);
  private toastrService = inject(ToastrService);
  private mobileObserver = inject(MobileObserver);

  protected loadingResults = signal(false);
  protected results = signal<number[]>([]);

  protected loadingLabels = signal(false);
  protected labels = signal<string[]>([]);

  protected isMobile = signal(false);

  protected sortedResults = computed<[string, number, number][]>(() => {
    const logits = this.results();
    const labels = this.labels();

    const maxLogit = Math.max(...logits);
    const exps = logits.map((x) => Math.exp(x - maxLogit));
    const sumExps = exps.reduce((acc, x) => acc + x, 0);
    const probs = exps.map((x) => x / sumExps);

    return probs
      .map((prob, i) => [labels[i], prob, 1] as [string, number, number])
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);
  });

  public ngOnInit(): void {
    this.mobileObserver.onMobileChange(this.isMobile.set);

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

    console.log(this.inputImage);

    if (!this.inputImage) {
      this.toastrService.error('Please upload image first.', 'No image uploaded.');
      return;
    }

    this.loadingResults.set(true);
    this.inferenceService.runInference(this.inputImage).subscribe({
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
