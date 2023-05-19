import { trial_button } from '../atomic_components/trial_button';

export class trialButtonFactory {
  create(trials: Array<string>): Array<trial_button> {
    const arrayOfTrials: Array<trial_button> = [];
    trials.forEach((trial) => {
      arrayOfTrials.push(
        new trial_button(
          'button',
          ['btn', 'btn-light', 'btn-md', 'trial_button'],
          [
            ['id', 'mybutton'],
            [
              'onclick',
              `
              alert("you clicked trial #1");
              `,
            ],
          ],
          'Trial #' + trial
        )
      );
    });
    return arrayOfTrials;
  }
}
