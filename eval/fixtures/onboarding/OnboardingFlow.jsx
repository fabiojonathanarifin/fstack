import { useState } from 'react';
import { View } from 'react-native';
import WelcomeStep from './steps/WelcomeStep';
import GoalStep from './steps/GoalStep';
import PlanReadyStep from './steps/PlanReadyStep';

const STEPS = [WelcomeStep, GoalStep, PlanReadyStep];

export default function OnboardingFlow({ onDone }) {
  const [index, setIndex] = useState(0);
  const Step = STEPS[index];
  const next = () => (index < STEPS.length - 1 ? setIndex(index + 1) : onDone());
  return (
    <View style={{ flex: 1 }}>
      <Step onNext={next} />
    </View>
  );
}
