import { BreakpointObserver } from '@angular/cdk/layout';
import { inject, Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class MobileObserver {
  private breakpointObserver = inject(BreakpointObserver);

  private observer$ = this.breakpointObserver.observe('(max-width: 1100px)');

  public onMobileChange(callback: (val: boolean) => void) {
    this.observer$.subscribe((state) => callback(state.matches));
  }
}
