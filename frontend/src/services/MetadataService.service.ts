import { Injectable } from "@angular/core";
import { map, Observable, shareReplay } from "rxjs";
import { HttpClientWrapper } from "./HttpClientWrapper.service";

@Injectable({
	providedIn: "root"
})
export class MetadataService {
	public constructor(
		private client: HttpClientWrapper
	) { }

	private labels$: Observable<string[]> | null = null;
	public getLabels(): Observable<string[]> {
		if (!this.labels$) {
			this.labels$ = this.client.getLabels().pipe(
				map(x => x.labels),
				shareReplay(1)
			);
		}

		return this.labels$;
	}

	private inputSize$: Observable<[number, number, number]> | null = null;
	public getInputSize(): Observable<[number, number, number]> {
		if (!this.inputSize$) {
			this.inputSize$ = this.client.getInputSize().pipe(
				map(x => x.input_size),
				shareReplay(1)
			);
		}

		return this.inputSize$;
	}
}