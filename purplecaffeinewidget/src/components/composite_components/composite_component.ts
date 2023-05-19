import { Atomic_Component } from '../atomic_components/atomic_components';

export class composite_component {
  div: Atomic_Component;

  constructor(css_classes?: Array<string>) {
    this.div = new Atomic_Component('div', css_classes);
  }

  appendChildren(children: Array<HTMLElement>): void {
    children.forEach((child) => {
      this.div.html_element.appendChild(child);
    });
  }
}
