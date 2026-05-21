import { Component, ElementRef, inject, OnInit, signal, ViewChild } from '@angular/core';
import { MetadataService } from '../services/MetadataService.service';
import { ToastrService } from 'ngx-toastr';
import { NgOptimizedImage } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css',
  imports: [NgOptimizedImage],
})
export class App implements OnInit {
  @ViewChild('previewCanvas') canvasRef!: ElementRef<HTMLCanvasElement>;

  protected hasImage = signal(false);
  async onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    // reset so the same file can be re-selected
    input.value = '';

    const [width, height] = [this.inputSize()[2], this.inputSize()[1]];
    console.log(width, height);
    const img = new Image();
    img.src = URL.createObjectURL(file);

    img.onload = () => {
      const ctx = this.canvasRef.nativeElement.getContext('2d')!;
      ctx.drawImage(img, 0, 0, width, height);
      URL.revokeObjectURL(img.src);
      this.hasImage.set(true);
    };
  }
  private metadataService = inject(MetadataService);
  private toastrService = inject(ToastrService);

  protected loadingLabels = signal(true);
  protected labels = signal<[string, number][]>([]);

  protected loadingInputSize = signal(true);
  protected inputSize = signal<[number, number, number]>([3, 384, 384]);

  public constructor() {}

  public ngOnInit(): void {
    this.loadLabels();
  }

  protected loadLabels() {
    this.loadingLabels.set(true);
    this.metadataService.getLabels().subscribe({
      next: (value) => this.setLabels(value),
      error: (err) => this.toastrService.error(err, 'Failed to load labels.'),
    });
  }

  private setLabels(labels: string[]) {
    this.labels.set(labels.map((v) => [v, 0]));
    this.loadingLabels.set(false);
  }

  protected loadInputSize() {
    this.loadingInputSize.set(true);
    this.metadataService.getInputSize().subscribe({
      next: (value) => this.setInputSize(value),
      error: (err) => this.toastrService.error(err, 'Failed to load input size.'),
    });
  }

  private setInputSize(inputSize: [number, number, number]) {
    this.inputSize.set([...inputSize]);
    this.loadingInputSize.set(false);
  }
}
