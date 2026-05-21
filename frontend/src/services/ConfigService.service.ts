import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ConfigService {
  public get baseApiUrl() {
    return 'http://localhost:5005';
  }

  public get versionSlug() {
    return '/api/v1';
  }

  private _endpoints = new Endpoints();
  public get endpoints() {
    return this._endpoints;
  }
}

class Endpoints {
  public readonly labels = '/metadata/labels';
  public readonly inputSize = '/metadata/input-size';
  public readonly inference = '/inference';
}
