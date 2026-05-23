import { inject, Injectable } from '@angular/core';
import { HttpClientWrapper } from './HttpClientWrapper.service';
import { map, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class InferenceService {
  private httpClient = inject(HttpClientWrapper);

  public runInference(image: Blob): Observable<number[]> {
    return this.httpClient.postInference(image).pipe(map((x) => x.predictions));
  }
}
