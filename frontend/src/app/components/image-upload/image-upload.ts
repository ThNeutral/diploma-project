import {
  Component,
  computed,
  ElementRef,
  EventEmitter,
  inject,
  Input,
  Output,
  signal,
  ViewChild,
} from '@angular/core';
import { NgOptimizedImage } from '@angular/common';
import { MetadataService } from '../../../services/MetadataService.service';
import { ToastrService } from 'ngx-toastr';
import { BreakpointObserver } from '@angular/cdk/layout';

@Component({
  selector: 'app-image-upload',
  imports: [NgOptimizedImage],
  templateUrl: './image-upload.html',
  styleUrl: './image-upload.css',
})
export class ImageUpload {
  @ViewChild('previewCanvas') protected canvasRef!: ElementRef<HTMLCanvasElement>;

  @Output() public onImageReady = new EventEmitter<ImageData>();

  private metadataService = inject(MetadataService);
  private toastrService = inject(ToastrService);
  private breakpointObserver = inject(BreakpointObserver);

  protected inputSize = signal<[number, number, number]>([3, 384, 384]);
  protected inputWidth = computed(() => this.inputSize()[1]);
  protected inputHeight = computed(() => this.inputSize()[2]);

  protected isDragging = signal(false);

  protected isMobile = signal(false);

  public constructor() {
    this.breakpointObserver
      .observe('(max-width: 1100px)')
      .subscribe((result) => this.isMobile.set(result.matches));
  }

  protected loadInputSize() {
    this.metadataService.getInputSize().subscribe({
      next: (value) => {
        this.inputSize.set([...value]);
      },
      error: (err) => {
        const message = err?.error?.message ?? err?.message ?? err;
        this.toastrService.error(message, 'Failed to load input size.');
      },
    });
  }

  protected onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(true);
  }

  protected onDragLeave() {
    this.isDragging.set(false);
  }

  protected onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(false);

    const file = event.dataTransfer?.files?.[0];
    if (!file || !file.type.startsWith('image/')) return;

    this.loadImage(file);
  }

  protected onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    input.value = '';
    this.loadImage(file);
  }

  protected loadImage(file: File) {
    const img = new Image();
    img.src = URL.createObjectURL(file);

    img.onload = () => {
      const canvas = this.canvasRef.nativeElement;
      const ctx = canvas.getContext('2d')!;
      ctx.drawImage(img, 0, 0, this.inputWidth(), this.inputHeight());
      URL.revokeObjectURL(img.src);

      const imageData = ctx.getImageData(0, 0, this.inputWidth(), this.inputHeight());

      this.onImageReady.emit(imageData);
    };
  }
}
