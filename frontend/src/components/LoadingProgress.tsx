import { useState, useEffect } from 'react';
import { Card, CardBody } from '@heroui/card';

interface LoadingProgressProps {
    mode: 'pdf' | 'chat';
    isLongPlanning?: boolean;
    isVisible: boolean;
}

const PDF_STEPS_NORMAL = [
    { label: 'Uploading PDF', duration: 5 },
    { label: 'Parsing PDF content', duration: 40 },
    { label: 'Extracting course data', duration: 40 },
    { label: 'Preparing AI agent', duration: 5 },
    { label: 'Generating response', duration: 30 },
    { label: 'Finalizing recommendations', duration: 25 },
    { label: 'Completing analysis', duration: 5 },
];

const PDF_STEPS_LONG = [
    { label: 'Uploading PDF', duration: 5 },
    { label: 'Parsing PDF content', duration: 40 },
    { label: 'Extracting course data', duration: 40 },
    { label: 'Preparing AI agent', duration: 5 },
    { label: 'Creating comprehensive plan', duration: 80 },
    { label: 'Validating course sequences', duration: 60 },
    { label: 'Finalizing recommendations', duration: 35 },
    { label: 'Completing analysis', duration: 5 },
];

const CHAT_STEPS_NORMAL = [
    { label: 'Processing your question', duration: 10 },
    { label: 'Analyzing degree requirements', duration: 20 },
    { label: 'Generating recommendations', duration: 20 },
    { label: 'Finalizing response', duration: 5 },
];

const CHAT_STEPS_LONG = [
    { label: 'Processing your question', duration: 15 },
    { label: 'Analyzing degree requirements', duration: 40 },
    { label: 'Creating comprehensive plan', duration: 70 },
    { label: 'Validating course sequences', duration: 40 },
    { label: 'Finalizing response', duration: 10 },
];

export default function LoadingProgress({
    mode,
    isLongPlanning = false,
    isVisible,
}: LoadingProgressProps) {
    const [currentStep, setCurrentStep] = useState(0);
    const [stepProgress, setStepProgress] = useState(0);
    const [overallProgress, setOverallProgress] = useState(0);

    const steps =
        mode === 'pdf'
            ? isLongPlanning
                ? PDF_STEPS_LONG
                : PDF_STEPS_NORMAL
            : isLongPlanning
              ? CHAT_STEPS_LONG
              : CHAT_STEPS_NORMAL;

    const totalDuration = steps.reduce((sum, step) => sum + step.duration, 0);

    useEffect(() => {
        if (!isVisible) {
            setCurrentStep(0);
            setStepProgress(0);
            setOverallProgress(0);
            return;
        }

        let stepStartTime = Date.now();
        let overallStartTime = Date.now();
        let currentStepIndex = 0;

        const updateProgress = () => {
            const elapsed = (Date.now() - overallStartTime) / 1000;
            const overallPercent = Math.min(
                (elapsed / totalDuration) * 100,
                95
            );

            setOverallProgress(overallPercent);

            // Calculate current step progress
            let accumulatedTime = 0;
            for (let i = 0; i < steps.length; i++) {
                if (i === currentStepIndex) {
                    const stepElapsed = (Date.now() - stepStartTime) / 1000;
                    const stepPercent = Math.min(
                        (stepElapsed / steps[i].duration) * 100,
                        100
                    );
                    setStepProgress(stepPercent);
                    setCurrentStep(i);

                    // Move to next step if current step is complete
                    if (
                        stepElapsed >= steps[i].duration &&
                        i < steps.length - 1
                    ) {
                        currentStepIndex = i + 1;
                        stepStartTime = Date.now();
                    }
                    break;
                }
                accumulatedTime += steps[i].duration;
            }
        };

        const interval = setInterval(updateProgress, 100);

        return () => clearInterval(interval);
    }, [isVisible, steps, totalDuration]);

    if (!isVisible) return null;

    return (
        <Card className="w-full mb-4" shadow="md">
            <CardBody className="p-6">
                <div className="space-y-4">
                    <div className="flex items-center justify-between mb-2">
                        <h3 className="text-lg font-semibold">
                            {mode === 'pdf'
                                ? 'Processing Your PDF'
                                : 'Generating Response'}
                        </h3>
                        <span className="text-sm text-default-500">
                            {Math.round(overallProgress)}%
                        </span>
                    </div>

                    {/* Overall Progress */}
                    <div className="w-full bg-default-200 rounded-full h-3 overflow-hidden">
                        <div
                            className="bg-gradient-to-r from-secondary-400 to-secondary-600 h-full rounded-full transition-all duration-300 ease-out"
                            style={{ width: `${overallProgress}%` }}
                        />
                    </div>

                    {/* Step List */}
                    <div className="space-y-2 mt-4">
                        {steps.map((step, index) => (
                            <div
                                key={index}
                                className={`flex items-center gap-3 p-2 rounded-lg transition-colors ${
                                    index === currentStep
                                        ? 'bg-secondary-50'
                                        : index < currentStep
                                          ? 'bg-success-50'
                                          : 'bg-default-50'
                                }`}
                            >
                                <div
                                    className={`w-2 h-2 rounded-full ${
                                        index === currentStep
                                            ? 'bg-secondary animate-pulse'
                                            : index < currentStep
                                              ? 'bg-success'
                                              : 'bg-default-300'
                                    }`}
                                />
                                <span
                                    className={`text-sm flex-1 ${
                                        index === currentStep
                                            ? 'font-semibold text-secondary'
                                            : index < currentStep
                                              ? 'text-success-600'
                                              : 'text-default-500'
                                    }`}
                                >
                                    {step.label}
                                </span>
                                {index === currentStep && (
                                    <span className="text-xs text-default-400">
                                        {Math.round(stepProgress)}%
                                    </span>
                                )}
                            </div>
                        ))}
                    </div>

                    <p className="text-xs text-default-500 text-center mt-4">
                        {mode === 'pdf'
                            ? isLongPlanning
                                ? 'This usually takes 4-5 minutes (70-90s PDF processing + 150-200s planning)'
                                : 'This usually takes 2-2.5 minutes (70-90s PDF processing + 50-60s response)'
                            : isLongPlanning
                              ? 'Long planning mode may take 2.5-3.5 minutes'
                              : 'This usually takes 50-60 seconds'}
                    </p>
                </div>
            </CardBody>
        </Card>
    );
}

