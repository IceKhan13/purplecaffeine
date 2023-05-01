// Copyright (c) purplecaffeine
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

export class WidgetModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: WidgetModel.model_name,
      _model_module: WidgetModel.model_module,
      _model_module_version: WidgetModel.model_module_version,
      _view_name: WidgetModel.view_name,
      _view_module: WidgetModel.view_module,
      _view_module_version: WidgetModel.view_module_version,
      value: 'Hello World',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'WidgetModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'WidgetView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class WidgetView extends DOMWidgetView {
  create_table_header(index: number, text: string): void {
    const headerCell1: HTMLTableCellElement = this.headerRow.insertCell(index);
    headerCell1.innerText = text;
  }

  private table: HTMLTableElement;
  private headerRow: HTMLTableRowElement;
  private headers: Array<string>;
  render(): void {
    this.table = document.createElement('table');
    this.headerRow = this.table.createTHead().insertRow(0);

    this.headers = ['coffe', 'price', 'location', 'other things'];
    let colNum = 0;
    this.headers.forEach((head: string) => {
      console.log(colNum, head);
      this.create_table_header(colNum, head);
      colNum += 1;
    });

    const row = this.table.insertRow(1);
    const cell1 = row.insertCell(0);
    const cell2 = row.insertCell(1);
    const cell3 = row.insertCell(2);
    const cell4 = row.insertCell(3);
    cell1.innerHTML = 'NEW CELL1';
    cell2.innerHTML = 'NEW CELL2';
    cell3.innerHTML = 'NEW CELL1';
    cell4.innerHTML = 'NEW CELL2';

    this.el.appendChild(this.table);
    console.log(this.el);
    this.el.classList.add('purplecaffeine');

    //this.value_changed();
    //this.model.on('change:value', this.value_changed, this);
  }
}
