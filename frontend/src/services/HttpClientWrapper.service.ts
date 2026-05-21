import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { ConfigService } from "./ConfigService.service";

@Injectable({
	providedIn: "root"
})
export class HttpClientWrapper {
	public constructor(
		private client: HttpClient,
		private config: ConfigService
	) { }

	public getLabels(): Observable<GetLabelsResponse> {
		var response: GetLabelsResponse = {
			labels: ["one", "two", "three"]
		};
		return new Observable(subcriber => {
			// subcriber.next(response);
			subcriber.error("Error");
			subcriber.complete();
		});

		const url = this.getApiUrl(this.config.endpoints.labels);
		return this.client.get<GetLabelsResponse>(url);
	}

	public getInputSize(): Observable<GetInputSizeResponse> {
		var response: GetInputSizeResponse = {
			input_size: [3, 384, 384]
		};
		return new Observable(subcriber => {
			subcriber.next(response);
			subcriber.complete();
		});
		
		const url = this.getApiUrl(this.config.endpoints.inputSize);
		return this.client.get<GetInputSizeResponse>(url);
	}

	private getApiUrl(endpoint: string) {
		return this.config.baseApiUrl + this.config.versionSlug + endpoint;
	}
}

interface GetLabelsResponse {
	labels: string[]
}

interface GetInputSizeResponse {
	input_size: [number, number, number]
}