import { inject, Injectable } from '@angular/core';
import { HttpClientWrapper } from './HttpClientWrapper.service';
import { map, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class InferenceService {
  private httpClient = inject(HttpClientWrapper);

  public runInference(
    image: ImageData,
    width: number,
    height: number,
  ): Observable<[number, number][]> {
    var buffer = new Uint8Array(image.data);
    return this.httpClient
      .postInference(buffer, width, height)
      .pipe(
        map((x) => Object.entries(x.results).map(([k, v]) => [Number(k), v] as [number, number])),
      );
  }
}
