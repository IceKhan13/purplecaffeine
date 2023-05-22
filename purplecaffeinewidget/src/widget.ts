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

import 'bootstrap/dist/css/bootstrap.min.css';

import 'bootstrap';
import { search_button } from './components/atomic_components/search_button';
import { search_bar } from './components/atomic_components/search_bar';
import { search_tools } from './components/composite_components/search_tool';
import { Atomic_Component } from './components/atomic_components/atomic_components';
import { trialButtonFactory } from './components/utils/trialButtonFactory';
import { list_of_trial_buttons } from './components/composite_components/list_of_trials_buttons';

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
      value: {},
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
  listOfTrials: list_of_trial_buttons;
  trial_button_factory = new trialButtonFactory();
  render(): void {
    const header = new Atomic_Component(
      'h1',
      ['header'],
      undefined,
      'PurpleCaffeine tracked trials'
    );

    this.listOfTrials = new list_of_trial_buttons(
      this.trial_button_factory.create(this.model.get('value')),
      ['list_of_trials']
    );
    const searchtools = new search_tools(
      new search_button(
        'button',
        ['btn', 'btn-primary', 'btn-lg'],
        [['id', 'mybutton']],
        'Search'
      ),
      new search_bar(
        'input',
        ['form-control', 'search_bar'],
        [
          ['aria-label', 'Big'],
          [
            'onchange',
            `
          alert();
          console.log("foo");
          `,
          ],
        ],
        'Trial #1'
      ),
      ['search_bar_and_button']
    );
    this.el.appendChild(header.html_element);
    this.el.appendChild(searchtools.div.html_element);
    this.el.appendChild(this.listOfTrials.div.html_element);

    this.model.on('change:value', this.value_changed, this);
  }

  value_changed(): void {
    this.el.removeChild(this.listOfTrials.div.html_element);
    this.listOfTrials = new list_of_trial_buttons(
      this.trial_button_factory.create(this.model.get('value')),
      ['list_of_trials']
    );
    this.el.appendChild(this.listOfTrials.div.html_element);
  }
}
