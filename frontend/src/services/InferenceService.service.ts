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
  ): Observable<[string, number][]> {
    return this.httpClient
      .postInference(image, width, height)
      .pipe(map((x) => x.top_five_candidates));
  }
}
