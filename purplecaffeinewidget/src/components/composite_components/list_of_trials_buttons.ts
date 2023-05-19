import { trial_button } from '../atomic_components/trial_button';
import { composite_component } from './composite_component';

export class list_of_trial_buttons extends composite_component {
  constructor(trials: Array<trial_button>, css_clases?: Array<string>) {
    super(css_clases);
    super.appendChildren(trials.map((trial) => trial.html_element));
  }
}
