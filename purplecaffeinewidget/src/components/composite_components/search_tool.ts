import { search_bar } from '../atomic_components/search_bar';
import { search_button } from '../atomic_components/search_button';
import { composite_component } from './composite_component';

export class search_tools extends composite_component {
  constructor(
    searchButton: search_button,
    input_text: search_bar,
    css_clases?: Array<string>
  ) {
    super(css_clases);
    this.appendChildren([input_text.html_element, searchButton.html_element]);
  }
}
