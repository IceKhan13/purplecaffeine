export class Atomic_Component {
  css_classes?: Array<string>;
  html_properties?: Array<Array<string>>;
  inner_html_label?: string;
  html_element: HTMLElement;
  html_type: string;

  constructor(
    html_type: string,
    css_classes?: Array<string>,
    html_properties?: Array<Array<string>>,
    inner_html_label?: string
  ) {
    this.html_type = html_type;
    this.html_properties = html_properties;
    this.css_classes = css_classes;
    this.html_element = document.createElement(html_type);
    if (inner_html_label !== undefined) {
      this.html_element.innerHTML = inner_html_label;
    }
    if (this.css_classes !== undefined) {
      this.css_classes.forEach((element) => {
        this.html_element.classList.add(element);
      });
    }
    if (this.html_properties !== undefined) {
      this.html_properties.forEach((element) => {
        if (element.length > 1) {
          this.html_element.setAttribute(element[0], element[1]);
        }
      });
    }
  }
}
