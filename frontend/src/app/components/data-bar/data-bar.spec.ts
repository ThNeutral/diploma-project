import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataBar } from './data-bar';

describe('DataBar', () => {
  let component: DataBar;
  let fixture: ComponentFixture<DataBar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DataBar],
    }).compileComponents();

    fixture = TestBed.createComponent(DataBar);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
