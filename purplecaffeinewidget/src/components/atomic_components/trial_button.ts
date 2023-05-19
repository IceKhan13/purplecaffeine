import { Atomic_Component } from './atomic_components';

export class trial_button extends Atomic_Component {
  action(): void {
    alert('It is alive');
  }

  constructor(
    html_type: string,
    css_classes?: Array<string>,
    html_properties?: Array<Array<string>>,
    inner_html_label?: string
  ) {
    super(html_type, css_classes, html_properties, inner_html_label);
  }
}
