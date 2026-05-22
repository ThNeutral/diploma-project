import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ConfigService } from './ConfigService.service';

@Injectable({
  providedIn: 'root',
})
export class HttpClientWrapper {
  public constructor(
    private client: HttpClient,
    private config: ConfigService,
  ) {}

  public getLabels(): Observable<GetLabelsResponse> {
    const url = this.getApiUrl(this.config.endpoints.labels);
    return this.client.get<GetLabelsResponse>(url);
  }

  public getInputSize(): Observable<GetInputSizeResponse> {
    const url = this.getApiUrl(this.config.endpoints.inputSize);
    return this.client.get<GetInputSizeResponse>(url);
  }

  public postInference(
    image: Uint8Array,
    width: number,
    height: number,
  ): Observable<PostInferenceResponse> {
    const response: PostInferenceResponse = {
      top_five_candidates: [
        ['Very Long Label aaaaaaaa aaaaaa aaa', Math.random()],
        ['b', Math.random()],
        ['c', Math.random()],
      ],
    };
    return new Observable((subscriber) => {
      subscriber.next(response);
      subscriber.complete();
    });

    const urlParams = new URLSearchParams({ width: '' + width, height: '' + height });
    const url = this.getApiUrl(this.config.endpoints.inputSize, urlParams);
    return this.client.post<PostInferenceResponse>(url, image, {
      headers: { 'Content-Type': 'application/octet-stream' },
    });
  }

  private getApiUrl(endpoint: string, urlParams?: URLSearchParams) {
    let url = this.config.baseApiUrl + this.config.versionSlug + endpoint;
    if (urlParams) {
      url += `?${urlParams}`;
    }

    return url;
  }
}

interface GetLabelsResponse {
  labels: string[];
}

interface GetInputSizeResponse {
  input_size: [number, number, number];
}

interface PostInferenceResponse {
  top_five_candidates: [string, number][];
}
