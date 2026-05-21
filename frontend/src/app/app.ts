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
  @ViewChild('previewCanvas') protected canvasRef!: ElementRef<HTMLCanvasElement>;

  private metadataService = inject(MetadataService);
  private toastrService = inject(ToastrService);

  protected loadingLabels = signal(true);
  protected labels = signal<[string, number][]>([]);

  protected loadingInputSize = signal(true);
  protected inputSize = signal<[number, number, number]>([3, 384, 384]);
  protected get imageWidth() {
    return this.inputSize()[2];
  }
  protected get imageHeight() {
    return this.inputSize()[1];
  }

  protected isDragging = signal(false);

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

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(true);
  }

  onDragLeave() {
    this.isDragging.set(false);
  }

  protected onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(false);

    const file = event.dataTransfer?.files?.[0];
    if (!file || !file.type.startsWith('image/')) return;

    this.loadImage(file);
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    input.value = '';
    this.loadImage(file);
  }

  loadImage(file: File) {
    const img = new Image();
    img.src = URL.createObjectURL(file);

    img.onload = () => {
      const ctx = this.canvasRef.nativeElement.getContext('2d')!;
      ctx.drawImage(img, 0, 0, this.imageWidth, this.imageHeight);
      URL.revokeObjectURL(img.src);
    };
  }
}
