BEGIN;

-- scam_sentinel.scam_sessions
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '4afa717a-5b46-4ea9-b97a-9753479d2d5f', '+918947382419', '+919730243887',
             NOW() - interval '371 hours',
             NOW() - interval '371 hours' + interval '4909 seconds',
             4909, 'AMBER', 83.4, 'cbi_impersonation', 'closing',
             '{"call_flow_match": {"score": 0.92}, "number_spoofing": {"score": 0.94}, "script_similarity": {"score": 0.93}, "voice_synthetic": {"score": 0.78}, "urgency_phrases": {"score": 0.81}}'::jsonb, false,
             NULL,
             false, 0.80, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '83 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '0a80944e-77cb-4458-bc6c-e3966087e958', '+917240251661', '+917983753977',
             NOW() - interval '624 hours',
             NOW() - interval '624 hours' + interval '5381 seconds',
             5381, 'AMBER', 65.0, 'bank_kyc', 'opening',
             '{"call_flow_match": {"score": 0.81}, "number_spoofing": {"score": 0.95}, "script_similarity": {"score": 0.84}, "voice_synthetic": {"score": 0.61}, "urgency_phrases": {"score": 0.91}}'::jsonb, false,
             NULL,
             true, 0.79, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '52e47607-ea8e-4691-af52-c71bac2afca1', '+919510777721', '+918840109255',
             NOW() - interval '323 hours',
             NOW() - interval '323 hours' + interval '1921 seconds',
             1921, 'AMBER', 69.6, 'tax_evasion', 'closing',
             '{"call_flow_match": {"score": 0.83}, "number_spoofing": {"score": 0.62}, "script_similarity": {"score": 0.69}, "voice_synthetic": {"score": 0.61}, "urgency_phrases": {"score": 0.78}}'::jsonb, true,
             '+919506254832',
             false, 0.54, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '112 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '929c72b0-b00b-4da1-8f27-cfe0c798c9f4', '+917049310608', '+919921794983',
             NOW() - interval '157 hours',
             NOW() - interval '157 hours' + interval '5320 seconds',
             5320, 'AMBER', 63.3, 'customs_seizure', 'opening',
             '{"call_flow_match": {"score": 0.81}, "number_spoofing": {"score": 0.77}, "script_similarity": {"score": 0.78}, "voice_synthetic": {"score": 0.44}, "urgency_phrases": {"score": 0.87}}'::jsonb, false,
             NULL,
             false, 0.73, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '137 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '36bf9a70-fce2-4994-82bb-12a72bedb490', '+919744267175', '+919180395476',
             NOW() - interval '465 hours',
             NOW() - interval '465 hours' + interval '206 seconds',
             206, 'RED', 95.5, 'digital_arrest', 'trust_building',
             '{"call_flow_match": {"score": 0.85}, "number_spoofing": {"score": 0.58}, "script_similarity": {"score": 0.95}, "voice_synthetic": {"score": 0.78}, "urgency_phrases": {"score": 0.79}}'::jsonb, true,
             '+919615507143',
             true, 0.42, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '2d0f276f-fbfa-45ca-bba1-f73d9d5b8fd2', '+917338258951', '+917367878761',
             NOW() - interval '614 hours',
             NOW() - interval '614 hours' + interval '2835 seconds',
             2835, 'YELLOW', 57.7, 'bank_kyc', 'opening',
             '{"call_flow_match": {"score": 0.99}, "number_spoofing": {"score": 0.86}, "script_similarity": {"score": 0.69}, "voice_synthetic": {"score": 0.43}, "urgency_phrases": {"score": 0.87}}'::jsonb, false,
             NULL,
             false, 0.74, 'acknowledged',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '70 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '672d7e22-63ee-4623-981f-66945d3e893d', '+919884873529', '+919791205006',
             NOW() - interval '170 hours',
             NOW() - interval '170 hours' + interval '2351 seconds',
             2351, 'AMBER', 72.8, 'customs_seizure', 'closing',
             '{"call_flow_match": {"score": 0.97}, "number_spoofing": {"score": 0.84}, "script_similarity": {"score": 0.86}, "voice_synthetic": {"score": 0.69}, "urgency_phrases": {"score": 0.82}}'::jsonb, false,
             NULL,
             false, 0.52, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '132 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '2094f741-34fe-4c9d-9931-c7930a9f59c5', '+919873237671', '+919084839399',
             NOW() - interval '236 hours',
             NOW() - interval '236 hours' + interval '5000 seconds',
             5000, 'RED', 91.3, 'digital_arrest', 'closing',
             '{"call_flow_match": {"score": 0.77}, "number_spoofing": {"score": 0.91}, "script_similarity": {"score": 0.93}, "voice_synthetic": {"score": 0.34}, "urgency_phrases": {"score": 0.77}}'::jsonb, false,
             NULL,
             false, 0.43, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '33 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'c1680aee-69b8-4f8e-a1d8-f1097908b1af', '+917260329455', '+918729245242',
             NOW() - interval '417 hours',
             NOW() - interval '417 hours' + interval '1739 seconds',
             1739, 'AMBER', 81.2, 'digital_arrest', 'payment_demand',
             '{"call_flow_match": {"score": 0.82}, "number_spoofing": {"score": 0.89}, "script_similarity": {"score": 0.62}, "voice_synthetic": {"score": 0.66}, "urgency_phrases": {"score": 0.89}}'::jsonb, false,
             NULL,
             false, 0.74, 'acknowledged',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '409 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '7482878e-124f-4125-868e-ab5259d2963a', '+917063384488', '+917400560567',
             NOW() - interval '188 hours',
             NOW() - interval '188 hours' + interval '2461 seconds',
             2461, 'AMBER', 66.0, 'cbi_impersonation', 'payment_demand',
             '{"call_flow_match": {"score": 0.93}, "number_spoofing": {"score": 0.89}, "script_similarity": {"score": 0.64}, "voice_synthetic": {"score": 0.66}, "urgency_phrases": {"score": 0.86}}'::jsonb, false,
             NULL,
             true, 0.86, 'active',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '207ac6ef-03fb-4d71-a386-109257492171', '+919387006772', '+919842715617',
             NOW() - interval '61 hours',
             NOW() - interval '61 hours' + interval '1528 seconds',
             1528, 'YELLOW', 44.1, 'digital_arrest', 'payment_demand',
             '{"call_flow_match": {"score": 0.93}, "number_spoofing": {"score": 0.7}, "script_similarity": {"score": 0.76}, "voice_synthetic": {"score": 0.83}, "urgency_phrases": {"score": 1.0}}'::jsonb, false,
             NULL,
             true, 0.73, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'b162c08d-dfae-4735-a882-e008978ba59e', '+919555656321', '+917291889680',
             NOW() - interval '63 hours',
             NOW() - interval '63 hours' + interval '2749 seconds',
             2749, 'AMBER', 67.1, 'cbi_impersonation', 'closing',
             '{"call_flow_match": {"score": 0.95}, "number_spoofing": {"score": 0.57}, "script_similarity": {"score": 0.97}, "voice_synthetic": {"score": 0.34}, "urgency_phrases": {"score": 0.76}}'::jsonb, false,
             NULL,
             false, 0.71, 'acknowledged',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '30 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'efe33db6-66f8-4d86-8672-3ea5794d99d6', '+919884887548', '+919772404776',
             NOW() - interval '635 hours',
             NOW() - interval '635 hours' + interval '851 seconds',
             851, 'AMBER', 82.6, 'cbi_impersonation', 'opening',
             '{"call_flow_match": {"score": 0.97}, "number_spoofing": {"score": 0.59}, "script_similarity": {"score": 0.87}, "voice_synthetic": {"score": 0.43}, "urgency_phrases": {"score": 0.82}}'::jsonb, false,
             NULL,
             false, 0.48, 'acknowledged',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '323 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '0be8be37-c926-4641-913f-e2b5c8f6f2ad', '+919333103372', '+918299301222',
             NOW() - interval '103 hours',
             NOW() - interval '103 hours' + interval '780 seconds',
             780, 'RED', 98.0, 'customs_seizure', 'closing',
             '{"call_flow_match": {"score": 0.8}, "number_spoofing": {"score": 0.53}, "script_similarity": {"score": 0.69}, "voice_synthetic": {"score": 0.46}, "urgency_phrases": {"score": 0.83}}'::jsonb, false,
             NULL,
             false, 0.67, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '237e85e6-9070-4be5-bbe4-55a04f32a5c7', '+917874443787', '+919952777682',
             NOW() - interval '680 hours',
             NOW() - interval '680 hours' + interval '1028 seconds',
             1028, 'YELLOW', 30.2, 'tax_evasion', 'fear_induction',
             '{"call_flow_match": {"score": 0.73}, "number_spoofing": {"score": 0.75}, "script_similarity": {"score": 0.7}, "voice_synthetic": {"score": 0.63}, "urgency_phrases": {"score": 0.92}}'::jsonb, true,
             '+919724031273',
             false, 0.81, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '218c6263-59dd-49ab-a90e-551d7ab2ab44', '+917323169889', '+919967906665',
             NOW() - interval '284 hours',
             NOW() - interval '284 hours' + interval '541 seconds',
             541, 'YELLOW', 56.3, 'digital_arrest', 'payment_demand',
             '{"call_flow_match": {"score": 0.78}, "number_spoofing": {"score": 0.83}, "script_similarity": {"score": 0.81}, "voice_synthetic": {"score": 0.54}, "urgency_phrases": {"score": 0.7}}'::jsonb, false,
             NULL,
             true, 0.84, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '279 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '81a03f0b-1bc1-47e1-9e45-e2225c5026fd', '+918745377599', '+919665720874',
             NOW() - interval '316 hours',
             NOW() - interval '316 hours' + interval '3167 seconds',
             3167, 'AMBER', 68.9, 'cbi_impersonation', 'opening',
             '{"call_flow_match": {"score": 0.96}, "number_spoofing": {"score": 0.59}, "script_similarity": {"score": 0.69}, "voice_synthetic": {"score": 0.36}, "urgency_phrases": {"score": 0.93}}'::jsonb, true,
             '+917663801533',
             true, 0.86, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '121 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '342b479a-1bf7-4042-902c-b91f5be8b117', '+917166320906', '+919021598245',
             NOW() - interval '184 hours',
             NOW() - interval '184 hours' + interval '2901 seconds',
             2901, 'AMBER', 83.4, 'tax_evasion', 'opening',
             '{"call_flow_match": {"score": 0.91}, "number_spoofing": {"score": 0.61}, "script_similarity": {"score": 0.66}, "voice_synthetic": {"score": 0.69}, "urgency_phrases": {"score": 0.81}}'::jsonb, true,
             '+917955345537',
             false, 0.42, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '117 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '82cce636-1538-42ce-9973-0a3ab79e8abe', '+917118543408', '+917495389030',
             NOW() - interval '409 hours',
             NOW() - interval '409 hours' + interval '2869 seconds',
             2869, 'YELLOW', 55.3, 'digital_arrest', 'trust_building',
             '{"call_flow_match": {"score": 0.8}, "number_spoofing": {"score": 0.73}, "script_similarity": {"score": 0.86}, "voice_synthetic": {"score": 0.76}, "urgency_phrases": {"score": 0.8}}'::jsonb, false,
             NULL,
             false, 0.83, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '133 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'b6ef4571-4be0-4cfa-9de4-f3a6ff989369', '+919312633708', '+919950028965',
             NOW() - interval '354 hours',
             NOW() - interval '354 hours' + interval '2749 seconds',
             2749, 'RED', 87.5, 'digital_arrest', 'payment_demand',
             '{"call_flow_match": {"score": 0.96}, "number_spoofing": {"score": 0.59}, "script_similarity": {"score": 0.62}, "voice_synthetic": {"score": 0.54}, "urgency_phrases": {"score": 0.86}}'::jsonb, false,
             NULL,
             true, 0.73, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '5e668567-6344-4a6a-9f98-1597a89cbaea', '+917823946934', '+918805803262',
             NOW() - interval '639 hours',
             NOW() - interval '639 hours' + interval '2751 seconds',
             2751, 'YELLOW', 40.6, 'digital_arrest', 'fear_induction',
             '{"call_flow_match": {"score": 0.85}, "number_spoofing": {"score": 0.8}, "script_similarity": {"score": 0.72}, "voice_synthetic": {"score": 0.68}, "urgency_phrases": {"score": 0.87}}'::jsonb, true,
             '+919855850145',
             false, 0.86, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '178 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '9719de06-a26d-4c21-aa22-80a2cf759ab9', '+917728818981', '+919829742424',
             NOW() - interval '216 hours',
             NOW() - interval '216 hours' + interval '3701 seconds',
             3701, 'AMBER', 67.2, 'digital_arrest', 'fear_induction',
             '{"call_flow_match": {"score": 0.83}, "number_spoofing": {"score": 0.8}, "script_similarity": {"score": 0.79}, "voice_synthetic": {"score": 0.74}, "urgency_phrases": {"score": 0.99}}'::jsonb, true,
             '+917364194056',
             false, 0.47, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '83112ecc-0921-4f57-b42d-c749188c779e', '+919704821724', '+919472487690',
             NOW() - interval '689 hours',
             NOW() - interval '689 hours' + interval '2722 seconds',
             2722, 'YELLOW', 32.7, 'bank_kyc', 'trust_building',
             '{"call_flow_match": {"score": 0.77}, "number_spoofing": {"score": 0.71}, "script_similarity": {"score": 0.92}, "voice_synthetic": {"score": 0.34}, "urgency_phrases": {"score": 0.82}}'::jsonb, false,
             NULL,
             false, 0.42, 'active',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '0969dda9-bb96-4da3-993c-605a14a04f66', '+918995627518', '+919867224513',
             NOW() - interval '110 hours',
             NOW() - interval '110 hours' + interval '3662 seconds',
             3662, 'YELLOW', 37.1, 'customs_seizure', 'opening',
             '{"call_flow_match": {"score": 0.83}, "number_spoofing": {"score": 0.75}, "script_similarity": {"score": 0.95}, "voice_synthetic": {"score": 0.37}, "urgency_phrases": {"score": 0.74}}'::jsonb, false,
             NULL,
             true, 0.62, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '71 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'bdb9ba1a-7a2e-43ca-aad3-810a9da6ca26', '+919081328344', '+919691864041',
             NOW() - interval '437 hours',
             NOW() - interval '437 hours' + interval '4668 seconds',
             4668, 'YELLOW', 55.9, 'customs_seizure', 'closing',
             '{"call_flow_match": {"score": 0.83}, "number_spoofing": {"score": 0.84}, "script_similarity": {"score": 0.92}, "voice_synthetic": {"score": 0.45}, "urgency_phrases": {"score": 0.93}}'::jsonb, false,
             NULL,
             false, 0.44, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '225 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '5be2594e-213e-4dd4-a54f-8deb6ce62bad', '+918804502687', '+918672790155',
             NOW() - interval '83 hours',
             NOW() - interval '83 hours' + interval '1313 seconds',
             1313, 'YELLOW', 37.9, 'digital_arrest', 'closing',
             '{"call_flow_match": {"score": 0.76}, "number_spoofing": {"score": 0.69}, "script_similarity": {"score": 0.73}, "voice_synthetic": {"score": 0.56}, "urgency_phrases": {"score": 0.72}}'::jsonb, false,
             NULL,
             false, 0.84, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '28f0a586-60bc-49aa-b4dc-ef02ef72b5aa', '+917947206476', '+919096929657',
             NOW() - interval '489 hours',
             NOW() - interval '489 hours' + interval '228 seconds',
             228, 'AMBER', 76.7, 'customs_seizure', 'payment_demand',
             '{"call_flow_match": {"score": 0.96}, "number_spoofing": {"score": 0.88}, "script_similarity": {"score": 0.8}, "voice_synthetic": {"score": 0.7}, "urgency_phrases": {"score": 0.94}}'::jsonb, true,
             '+917942408767',
             false, 0.46, 'acknowledged',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '248 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '7ae37966-8a2c-4cbb-bb31-637ba75424fc', '+917780520225', '+917215970859',
             NOW() - interval '479 hours',
             NOW() - interval '479 hours' + interval '1225 seconds',
             1225, 'AMBER', 68.1, 'cbi_impersonation', 'trust_building',
             '{"call_flow_match": {"score": 0.87}, "number_spoofing": {"score": 0.8}, "script_similarity": {"score": 0.63}, "voice_synthetic": {"score": 0.54}, "urgency_phrases": {"score": 0.96}}'::jsonb, true,
             '+918117362852',
             false, 0.53, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '108 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '5d73f5b0-a151-4753-a699-12530697500e', '+917133272825', '+918062073697',
             NOW() - interval '259 hours',
             NOW() - interval '259 hours' + interval '850 seconds',
             850, 'AMBER', 68.1, 'digital_arrest', 'payment_demand',
             '{"call_flow_match": {"score": 0.98}, "number_spoofing": {"score": 0.6}, "script_similarity": {"score": 0.63}, "voice_synthetic": {"score": 0.83}, "urgency_phrases": {"score": 0.71}}'::jsonb, false,
             NULL,
             true, 0.42, 'active',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'e4d9c28b-8290-42ad-8a68-f6247aa914ed', '+917464280597', '+919485432021',
             NOW() - interval '224 hours',
             NOW() - interval '224 hours' + interval '3989 seconds',
             3989, 'YELLOW', 33.7, 'customs_seizure', 'closing',
             '{"call_flow_match": {"score": 0.88}, "number_spoofing": {"score": 0.84}, "script_similarity": {"score": 0.64}, "voice_synthetic": {"score": 0.75}, "urgency_phrases": {"score": 0.99}}'::jsonb, true,
             '+917110287971',
             true, 0.86, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'c54cfb93-f8a1-492c-97f5-032c9e3b754f', '+917176390590', '+918491228808',
             NOW() - interval '78 hours',
             NOW() - interval '78 hours' + interval '5030 seconds',
             5030, 'YELLOW', 40.9, 'bank_kyc', 'trust_building',
             '{"call_flow_match": {"score": 0.92}, "number_spoofing": {"score": 0.88}, "script_similarity": {"score": 0.83}, "voice_synthetic": {"score": 0.37}, "urgency_phrases": {"score": 1.0}}'::jsonb, true,
             '+919288123416',
             false, 0.56, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '8cf58574-b279-4b7a-ae33-5721913b6653', '+919311435034', '+919076605983',
             NOW() - interval '109 hours',
             NOW() - interval '109 hours' + interval '3731 seconds',
             3731, 'YELLOW', 39.9, 'tax_evasion', 'payment_demand',
             '{"call_flow_match": {"score": 0.91}, "number_spoofing": {"score": 0.7}, "script_similarity": {"score": 0.88}, "voice_synthetic": {"score": 0.83}, "urgency_phrases": {"score": 0.78}}'::jsonb, true,
             '+918996617659',
             false, 0.56, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '93 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'c1368a3e-9c2b-4d92-b2e8-d745c9111dbd', '+918109615163', '+918461744198',
             NOW() - interval '462 hours',
             NOW() - interval '462 hours' + interval '2177 seconds',
             2177, 'YELLOW', 37.1, 'bank_kyc', 'fear_induction',
             '{"call_flow_match": {"score": 0.8}, "number_spoofing": {"score": 0.72}, "script_similarity": {"score": 0.72}, "voice_synthetic": {"score": 0.57}, "urgency_phrases": {"score": 0.81}}'::jsonb, true,
             '+918201124041',
             false, 0.83, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '359 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'e3ef2820-b772-43e5-bf31-c73732989774', '+918044987715', '+918315144891',
             NOW() - interval '417 hours',
             NOW() - interval '417 hours' + interval '4182 seconds',
             4182, 'YELLOW', 45.0, 'digital_arrest', 'trust_building',
             '{"call_flow_match": {"score": 0.91}, "number_spoofing": {"score": 0.7}, "script_similarity": {"score": 0.61}, "voice_synthetic": {"score": 0.46}, "urgency_phrases": {"score": 0.82}}'::jsonb, true,
             '+919851686578',
             false, 0.65, 'acknowledged',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '242 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '18710d2f-83bf-4b03-85d6-4759d388befa', '+917929364954', '+919079617090',
             NOW() - interval '720 hours',
             NOW() - interval '720 hours' + interval '3897 seconds',
             3897, 'AMBER', 68.3, 'cbi_impersonation', 'fear_induction',
             '{"call_flow_match": {"score": 0.76}, "number_spoofing": {"score": 0.55}, "script_similarity": {"score": 0.8}, "voice_synthetic": {"score": 0.72}, "urgency_phrases": {"score": 0.76}}'::jsonb, false,
             NULL,
             false, 0.47, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'fdebfef0-397c-40e7-b066-dff22d7e9f0c', '+919739629302', '+919108307952',
             NOW() - interval '304 hours',
             NOW() - interval '304 hours' + interval '2043 seconds',
             2043, 'YELLOW', 47.3, 'bank_kyc', 'trust_building',
             '{"call_flow_match": {"score": 0.74}, "number_spoofing": {"score": 0.52}, "script_similarity": {"score": 0.62}, "voice_synthetic": {"score": 0.46}, "urgency_phrases": {"score": 0.98}}'::jsonb, false,
             NULL,
             false, 0.36, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '6 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'fd255f89-aeb9-4119-91ce-be6428764714', '+917365849190', '+918065972034',
             NOW() - interval '259 hours',
             NOW() - interval '259 hours' + interval '4093 seconds',
             4093, 'YELLOW', 42.8, 'digital_arrest', 'opening',
             '{"call_flow_match": {"score": 0.87}, "number_spoofing": {"score": 0.81}, "script_similarity": {"score": 0.66}, "voice_synthetic": {"score": 0.75}, "urgency_phrases": {"score": 0.98}}'::jsonb, false,
             NULL,
             false, 0.37, 'acknowledged',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '213 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '80fe4fc0-af4d-4c05-93b6-fa29fd690636', '+917906346324', '+918136646449',
             NOW() - interval '454 hours',
             NOW() - interval '454 hours' + interval '2615 seconds',
             2615, 'RED', 93.5, 'cbi_impersonation', 'payment_demand',
             '{"call_flow_match": {"score": 0.88}, "number_spoofing": {"score": 0.77}, "script_similarity": {"score": 0.88}, "voice_synthetic": {"score": 0.82}, "urgency_phrases": {"score": 0.76}}'::jsonb, true,
             '+919836517266',
             true, 0.35, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '7c6ed4d4-7e1f-419e-b4c6-102323f5e96f', '+919533126989', '+919839759520',
             NOW() - interval '482 hours',
             NOW() - interval '482 hours' + interval '2565 seconds',
             2565, 'AMBER', 73.2, 'cbi_impersonation', 'closing',
             '{"call_flow_match": {"score": 0.95}, "number_spoofing": {"score": 0.53}, "script_similarity": {"score": 0.69}, "voice_synthetic": {"score": 0.45}, "urgency_phrases": {"score": 0.94}}'::jsonb, false,
             NULL,
             false, 0.78, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '7759ecb7-b6ad-4f33-b750-2fbb0c6f1eef', '+918728760924', '+918169288485',
             NOW() - interval '146 hours',
             NOW() - interval '146 hours' + interval '764 seconds',
             764, 'YELLOW', 36.5, 'digital_arrest', 'fear_induction',
             '{"call_flow_match": {"score": 0.94}, "number_spoofing": {"score": 0.91}, "script_similarity": {"score": 0.77}, "voice_synthetic": {"score": 0.56}, "urgency_phrases": {"score": 0.79}}'::jsonb, false,
             NULL,
             true, 0.60, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '126 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '70faa83f-9735-44e3-b393-1f7b6520e43e', '+917172793727', '+917752438459',
             NOW() - interval '257 hours',
             NOW() - interval '257 hours' + interval '391 seconds',
             391, 'RED', 91.1, 'customs_seizure', 'closing',
             '{"call_flow_match": {"score": 0.87}, "number_spoofing": {"score": 0.93}, "script_similarity": {"score": 0.98}, "voice_synthetic": {"score": 0.67}, "urgency_phrases": {"score": 0.78}}'::jsonb, false,
             NULL,
             true, 0.58, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '226 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '6a8410e5-359f-402b-b99f-f3bd06e1b873', '+919362646960', '+917157612991',
             NOW() - interval '94 hours',
             NOW() - interval '94 hours' + interval '4030 seconds',
             4030, 'YELLOW', 47.0, 'customs_seizure', 'payment_demand',
             '{"call_flow_match": {"score": 0.95}, "number_spoofing": {"score": 0.65}, "script_similarity": {"score": 0.86}, "voice_synthetic": {"score": 0.46}, "urgency_phrases": {"score": 0.98}}'::jsonb, false,
             NULL,
             false, 0.57, 'investigating',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '40 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'c0ab98c0-b019-48b7-8129-449762a1a4fe', '+917562697526', '+918237075775',
             NOW() - interval '674 hours',
             NOW() - interval '674 hours' + interval '4624 seconds',
             4624, 'RED', 88.5, 'tax_evasion', 'opening',
             '{"call_flow_match": {"score": 0.88}, "number_spoofing": {"score": 0.72}, "script_similarity": {"score": 0.77}, "voice_synthetic": {"score": 0.33}, "urgency_phrases": {"score": 0.78}}'::jsonb, false,
             NULL,
             false, 0.56, 'acknowledged',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '496 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '550ba85d-183e-45fe-bba6-bfdd04a64289', '+918253535854', '+919185588660',
             NOW() - interval '319 hours',
             NOW() - interval '319 hours' + interval '4692 seconds',
             4692, 'RED', 86.7, 'digital_arrest', 'trust_building',
             '{"call_flow_match": {"score": 0.94}, "number_spoofing": {"score": 0.55}, "script_similarity": {"score": 0.96}, "voice_synthetic": {"score": 0.66}, "urgency_phrases": {"score": 0.75}}'::jsonb, false,
             NULL,
             false, 0.72, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '1999ffdb-9d3a-4957-bf27-bf398dfb1f5b', '+919180716723', '+918147497835',
             NOW() - interval '393 hours',
             NOW() - interval '393 hours' + interval '1741 seconds',
             1741, 'AMBER', 71.6, 'cbi_impersonation', 'trust_building',
             '{"call_flow_match": {"score": 0.95}, "number_spoofing": {"score": 0.62}, "script_similarity": {"score": 0.9}, "voice_synthetic": {"score": 0.53}, "urgency_phrases": {"score": 0.98}}'::jsonb, true,
             '+917011017705',
             false, 0.47, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '152 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '36fa2c38-b70d-406e-932d-e0929a459702', '+918003143045', '+918764265618',
             NOW() - interval '552 hours',
             NOW() - interval '552 hours' + interval '4147 seconds',
             4147, 'AMBER', 73.9, 'tax_evasion', 'payment_demand',
             '{"call_flow_match": {"score": 0.83}, "number_spoofing": {"score": 0.64}, "script_similarity": {"score": 0.67}, "voice_synthetic": {"score": 0.68}, "urgency_phrases": {"score": 0.87}}'::jsonb, false,
             NULL,
             false, 0.33, 'acknowledged',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '484 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'ef1a5818-a978-4cce-84aa-f849519fbee3', '+917619142798', '+918760844750',
             NOW() - interval '508 hours',
             NOW() - interval '508 hours' + interval '483 seconds',
             483, 'AMBER', 79.5, 'customs_seizure', 'trust_building',
             '{"call_flow_match": {"score": 0.73}, "number_spoofing": {"score": 0.88}, "script_similarity": {"score": 0.64}, "voice_synthetic": {"score": 0.8}, "urgency_phrases": {"score": 0.7}}'::jsonb, false,
             NULL,
             true, 0.82, 'classified',
             NULL,
             NULL
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '5712e5f0-d9f0-429f-9485-fdfa5c948456', '+919323646093', '+917154185462',
             NOW() - interval '710 hours',
             NOW() - interval '710 hours' + interval '3436 seconds',
             3436, 'RED', 98.6, 'digital_arrest', 'closing',
             '{"call_flow_match": {"score": 0.95}, "number_spoofing": {"score": 0.67}, "script_similarity": {"score": 0.72}, "voice_synthetic": {"score": 0.7}, "urgency_phrases": {"score": 0.93}}'::jsonb, true,
             '+919651968205',
             true, 0.34, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '646 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '62c1a471-34d2-4bd6-b357-49579887aedc', '+919281341978', '+918769748771',
             NOW() - interval '649 hours',
             NOW() - interval '649 hours' + interval '1003 seconds',
             1003, 'RED', 94.6, 'digital_arrest', 'opening',
             '{"call_flow_match": {"score": 0.71}, "number_spoofing": {"score": 0.86}, "script_similarity": {"score": 0.71}, "voice_synthetic": {"score": 0.51}, "urgency_phrases": {"score": 0.74}}'::jsonb, false,
             NULL,
             false, 0.64, 'closed',
             (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'),
             NOW() - interval '184 hours'
            );
INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             'ae3a514c-871b-4ff6-a988-1093aa5fc7bc', '+917678500147', '+917317234448',
             NOW() - interval '510 hours',
             NOW() - interval '510 hours' + interval '4957 seconds',
             4957, 'YELLOW', 55.3, 'customs_seizure', 'trust_building',
             '{"call_flow_match": {"score": 0.77}, "number_spoofing": {"score": 0.5}, "script_similarity": {"score": 0.91}, "voice_synthetic": {"score": 0.8}, "urgency_phrases": {"score": 0.9}}'::jsonb, false,
             NULL,
             false, 0.57, 'classified',
             NULL,
             NULL
            );

-- scam_sentinel.number_reputation
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919827075539', 89, 8,
             40,
             true,
             'customs_seizure',
             'Jio',
             NOW() - interval '672 days',
             NOW() - interval '41 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919456389272', 50, 3,
             0,
             false,
             NULL,
             'Vi',
             NOW() - interval '164 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918652244897', 18, 2,
             2,
             false,
             NULL,
             'BSNL',
             NOW() - interval '209 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918074163698', 50, 2,
             2,
             false,
             NULL,
             'Vi',
             NOW() - interval '198 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918268006448', 52, 3,
             1,
             false,
             NULL,
             'Vi',
             NOW() - interval '147 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918284857706', 4, 1,
             0,
             false,
             NULL,
             'BSNL',
             NOW() - interval '600 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+917458072318', 50, 3,
             0,
             false,
             NULL,
             'Vi',
             NOW() - interval '579 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919604496061', 23, 2,
             2,
             false,
             NULL,
             'BSNL',
             NOW() - interval '683 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918270762239', 73, 30,
             1,
             true,
             'cbi_impersonation',
             'Vi',
             NOW() - interval '654 days',
             NOW() - interval '14 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+917034780500', 90, 19,
             41,
             true,
             'tax_evasion',
             'BSNL',
             NOW() - interval '149 days',
             NOW() - interval '8 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+917940617318', 2, 2,
             1,
             false,
             NULL,
             'Jio',
             NOW() - interval '129 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919523601252', 34, 1,
             1,
             false,
             NULL,
             'BSNL',
             NOW() - interval '409 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919468798461', 93, 26,
             37,
             true,
             'bank_kyc',
             'Airtel',
             NOW() - interval '454 days',
             NOW() - interval '41 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919075362821', 31, 3,
             1,
             false,
             NULL,
             'Jio',
             NOW() - interval '409 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919607324296', 28, 1,
             1,
             false,
             NULL,
             'Jio',
             NOW() - interval '406 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918822393017', 90, 3,
             25,
             true,
             'customs_seizure',
             'Vi',
             NOW() - interval '224 days',
             NOW() - interval '7 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+917210643427', 96, 5,
             42,
             true,
             'tax_evasion',
             'Airtel',
             NOW() - interval '687 days',
             NOW() - interval '40 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919133427445', 70, 21,
             15,
             true,
             'digital_arrest',
             'Airtel',
             NOW() - interval '608 days',
             NOW() - interval '13 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918541717841', 48, 1,
             2,
             false,
             NULL,
             'Airtel',
             NOW() - interval '268 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918962094851', 9, 0,
             1,
             false,
             NULL,
             'Airtel',
             NOW() - interval '163 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918018790736', 95, 7,
             42,
             true,
             'cbi_impersonation',
             'Jio',
             NOW() - interval '164 days',
             NOW() - interval '0 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919430646623', 50, 1,
             2,
             false,
             NULL,
             'Vi',
             NOW() - interval '46 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918297602688', 3, 1,
             2,
             false,
             NULL,
             'BSNL',
             NOW() - interval '568 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918513206988', 4, 3,
             1,
             false,
             NULL,
             'Vi',
             NOW() - interval '555 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919964873967', 84, 14,
             39,
             true,
             'bank_kyc',
             'Jio',
             NOW() - interval '704 days',
             NOW() - interval '33 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918178884276', 41, 0,
             0,
             false,
             NULL,
             'BSNL',
             NOW() - interval '441 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918229194523', 6, 3,
             2,
             false,
             NULL,
             'BSNL',
             NOW() - interval '105 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+917855630484', 80, 9,
             4,
             true,
             'bank_kyc',
             'Airtel',
             NOW() - interval '311 days',
             NOW() - interval '39 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918484193033', 87, 24,
             38,
             true,
             'customs_seizure',
             'Vi',
             NOW() - interval '494 days',
             NOW() - interval '32 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919744220825', 73, 35,
             46,
             true,
             'digital_arrest',
             'Airtel',
             NOW() - interval '470 days',
             NOW() - interval '28 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+917094229853', 83, 29,
             25,
             true,
             'customs_seizure',
             'BSNL',
             NOW() - interval '127 days',
             NOW() - interval '20 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918699972733', 42, 2,
             1,
             false,
             NULL,
             'Airtel',
             NOW() - interval '515 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+919945486396', 53, 0,
             0,
             false,
             NULL,
             'BSNL',
             NOW() - interval '128 days',
             NULL,
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+918637947177', 81, 35,
             3,
             true,
             'cbi_impersonation',
             'Vi',
             NOW() - interval '716 days',
             NOW() - interval '7 days',
             '{}'::jsonb
            );
INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '+917988350974', 55, 3,
             2,
             false,
             NULL,
             'Jio',
             NOW() - interval '324 days',
             NULL,
             '{}'::jsonb
            );

-- scam_sentinel.scam_script_corpus
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '5a426c6b-ce9f-4550-aad1-04d3f3223b68', 'en', 'customs_seizure', 'Customs Parcel Seizure Scam', 'This is customs department Mumbai airport. A parcel booked under your name has been seized, containing banned items and cash worth lakhs. Pay the customs penalty now to avoid FIR.',
             '{"parcel seized","customs penalty","banned items","pay now"}', 26, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '6c7ac407-1f23-4820-af06-7b64076489af', 'hi', 'bank_kyc', 'बैंक केवाईसी समाप्ति धोखाधड़ी', 'प्रिय ग्राहक, आपके बैंक खाते का केवाईसी 2 घंटे में ब्लॉक हो जाएगा। खाता सक्रिय रखने के लिए तुरंत अपने फोन पर आया ओटीपी साझा करें।',
             '{"केवाईसी ब्लॉक","ओटीपी साझा करें","खाता निलंबन"}', 39, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '8d3d419b-aad5-4798-91bf-a87e15803417', 'en', 'bank_kyc', 'Bank KYC Expiry Fraud', 'Dear customer, your bank account KYC will be blocked within 2 hours. Share the OTP sent to your phone immediately to keep your account active and avoid permanent suspension.',
             '{"KYC will be blocked","share the OTP","account suspension","keep account active"}', 27, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'fce80606-9cae-4416-91d2-736ec10eac91', 'hi', 'customs_seizure', 'सीमा शुल्क पार्सल जब्ती घोटाला', 'यह मुंबई एयरपोर्ट सीमा शुल्क विभाग है। आपके नाम से बुक पार्सल जब्त हुआ है जिसमें प्रतिबंधित सामान है। एफआईआर से बचने के लिए अभी जुर्माना भरें।',
             '{"पार्सल जब्त","जुर्माना भरें","प्रतिबंधित सामान","एफआईआर से बचें"}', 142, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'e93c8d17-db01-4f1b-bf0f-274b2ff04e27', 'hi', 'customs_seizure', 'सीमा शुल्क पार्सल जब्ती घोटाला', 'यह मुंबई एयरपोर्ट सीमा शुल्क विभाग है। आपके नाम से बुक पार्सल जब्त हुआ है जिसमें प्रतिबंधित सामान है। एफआईआर से बचने के लिए अभी जुर्माना भरें।',
             '{"पार्सल जब्त","जुर्माना भरें","प्रतिबंधित सामान","एफआईआर से बचें"}', 195, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '2b5b63ce-0b7b-40c2-8aa6-6c7b95cdc228', 'en', 'customs_seizure', 'Customs Parcel Seizure Scam', 'This is customs department Mumbai airport. A parcel booked under your name has been seized, containing banned items and cash worth lakhs. Pay the customs penalty now to avoid FIR.',
             '{"parcel seized","customs penalty","banned items","pay now"}', 57, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '0ca6de90-bc84-49f2-9de3-f0b35ed12c20', 'en', 'tax_evasion', 'Income Tax Department Threat Call', 'This call is from the Income Tax Department, Investigation Wing. Discrepancies worth several lakhs have been found in your recent filings. A non-bailable warrant is being prepared unless you settle the pending dues today via UPI.',
             '{"income tax department","non-bailable warrant","settle dues","pay via UPI"}', 143, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'f207e801-7508-4b2c-bdd1-83f70575369d', 'hi', 'bank_kyc', 'बैंक केवाईसी समाप्ति धोखाधड़ी', 'प्रिय ग्राहक, आपके बैंक खाते का केवाईसी 2 घंटे में ब्लॉक हो जाएगा। खाता सक्रिय रखने के लिए तुरंत अपने फोन पर आया ओटीपी साझा करें।',
             '{"केवाईसी ब्लॉक","ओटीपी साझा करें","खाता निलंबन"}', 155, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '5fa73bcf-4dfa-4950-b3f1-4d45b7372a46', 'en', 'customs_seizure', 'Customs Parcel Seizure Scam', 'This is customs department Mumbai airport. A parcel booked under your name has been seized, containing banned items and cash worth lakhs. Pay the customs penalty now to avoid FIR.',
             '{"parcel seized","customs penalty","banned items","pay now"}', 46, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'da68ee51-4c29-447e-9c9e-7be89301c5f5', 'en', 'customs_seizure', 'Customs Parcel Seizure Scam', 'This is customs department Mumbai airport. A parcel booked under your name has been seized, containing banned items and cash worth lakhs. Pay the customs penalty now to avoid FIR.',
             '{"parcel seized","customs penalty","banned items","pay now"}', 195, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '269ca072-e9a6-4bf3-8c92-030a3a31db5b', 'en', 'customs_seizure', 'Customs Parcel Seizure Scam', 'This is customs department Mumbai airport. A parcel booked under your name has been seized, containing banned items and cash worth lakhs. Pay the customs penalty now to avoid FIR.',
             '{"parcel seized","customs penalty","banned items","pay now"}', 89, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'd417765f-be2f-4654-89b5-d0f0806a9f51', 'en', 'digital_arrest', 'Fake CBI Digital Arrest — Parcel Warning', 'This is Officer Verma from CBI Mumbai. Your Aadhaar-linked parcel containing illegal substances has been intercepted at customs. You are under digital arrest. Do not disconnect this call or contact anyone, or a warrant will be issued for your arrest.',
             '{"digital arrest","do not disconnect","warrant","aadhaar linked","customs intercepted"}', 36, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '332341d8-3f26-450d-892b-593e4f71bd74', 'en', 'tax_evasion', 'Income Tax Department Threat Call', 'This call is from the Income Tax Department, Investigation Wing. Discrepancies worth several lakhs have been found in your recent filings. A non-bailable warrant is being prepared unless you settle the pending dues today via UPI.',
             '{"income tax department","non-bailable warrant","settle dues","pay via UPI"}', 36, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '9405a0e0-4f6d-4e49-8b12-9df19ee356f4', 'en', 'digital_arrest', 'Fake CBI Digital Arrest — Parcel Warning', 'This is Officer Sharma from CBI Mumbai. Your Aadhaar-linked parcel containing illegal substances has been intercepted at customs. You are under digital arrest. Do not disconnect this call or contact anyone, or a warrant will be issued for your arrest.',
             '{"digital arrest","do not disconnect","warrant","aadhaar linked","customs intercepted"}', 191, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'af984231-6a33-4193-a55f-ca03a2306ba9', 'hi', 'bank_kyc', 'बैंक केवाईसी समाप्ति धोखाधड़ी', 'प्रिय ग्राहक, आपके बैंक खाते का केवाईसी 2 घंटे में ब्लॉक हो जाएगा। खाता सक्रिय रखने के लिए तुरंत अपने फोन पर आया ओटीपी साझा करें।',
             '{"केवाईसी ब्लॉक","ओटीपी साझा करें","खाता निलंबन"}', 96, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'cf032b12-02df-4a16-812a-695125557084', 'en', 'tax_evasion', 'Income Tax Department Threat Call', 'This call is from the Income Tax Department, Investigation Wing. Discrepancies worth several lakhs have been found in your recent filings. A non-bailable warrant is being prepared unless you settle the pending dues today via UPI.',
             '{"income tax department","non-bailable warrant","settle dues","pay via UPI"}', 87, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'a9b79742-9bc9-42e5-80a2-e49d3dd6756b', 'en', 'cbi_impersonation', 'CBI Impersonation — FIR Threat', 'We are calling from CBI Delhi headquarters. An FIR has been registered against your name in a money laundering case. To avoid immediate arrest, you must verify your bank account on this call.',
             '{"FIR registered","money laundering","immediate arrest","verify bank account"}', 79, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '4228ffe6-54f3-414e-b892-9bd2da2151e3', 'hi', 'customs_seizure', 'सीमा शुल्क पार्सल जब्ती घोटाला', 'यह मुंबई एयरपोर्ट सीमा शुल्क विभाग है। आपके नाम से बुक पार्सल जब्त हुआ है जिसमें प्रतिबंधित सामान है। एफआईआर से बचने के लिए अभी जुर्माना भरें।',
             '{"पार्सल जब्त","जुर्माना भरें","प्रतिबंधित सामान","एफआईआर से बचें"}', 145, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'ac39220b-d7b2-42a0-be60-f623db5d1851', 'hi', 'digital_arrest', 'फर्जी सीबीआई डिजिटल गिरफ्तारी — पार्सल चेतावनी', 'मैं सीबीआई मुंबई से अधिकारी Sharma बोल रहा हूं। आपके आधार से जुड़े पार्सल में अवैध सामान मिला है। आप डिजिटल गिरफ्तारी में हैं। कॉल मत काटिए वरना गिरफ्तारी वारंट जारी होगा।',
             '{"डिजिटल गिरफ्तारी","कॉल मत काटिए","वारंट","आधार लिंक"}', 39, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '1c3fe8ac-1464-44b4-9338-a08e393bb82d', 'en', 'cbi_impersonation', 'CBI Impersonation — FIR Threat', 'We are calling from CBI Delhi headquarters. An FIR has been registered against your name in a money laundering case. To avoid immediate arrest, you must verify your bank account on this call.',
             '{"FIR registered","money laundering","immediate arrest","verify bank account"}', 158, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'c6cb4136-79c1-48b8-9b1b-6437fdf3f43d', 'en', 'digital_arrest', 'Fake CBI Digital Arrest — Parcel Warning', 'This is Officer Rao from CBI Mumbai. Your Aadhaar-linked parcel containing illegal substances has been intercepted at customs. You are under digital arrest. Do not disconnect this call or contact anyone, or a warrant will be issued for your arrest.',
             '{"digital arrest","do not disconnect","warrant","aadhaar linked","customs intercepted"}', 20, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '3c385769-2ba5-4d70-8ad2-be81895fcf55', 'en', 'customs_seizure', 'Customs Parcel Seizure Scam', 'This is customs department Mumbai airport. A parcel booked under your name has been seized, containing banned items and cash worth lakhs. Pay the customs penalty now to avoid FIR.',
             '{"parcel seized","customs penalty","banned items","pay now"}', 169, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '48e37187-17cd-4c5a-854b-f72605a7fc78', 'en', 'tax_evasion', 'Income Tax Department Threat Call', 'This call is from the Income Tax Department, Investigation Wing. Discrepancies worth several lakhs have been found in your recent filings. A non-bailable warrant is being prepared unless you settle the pending dues today via UPI.',
             '{"income tax department","non-bailable warrant","settle dues","pay via UPI"}', 155, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'e21e5200-f711-4b60-ab7b-83baacc7c4cf', 'en', 'bank_kyc', 'Bank KYC Expiry Fraud', 'Dear customer, your bank account KYC will be blocked within 2 hours. Share the OTP sent to your phone immediately to keep your account active and avoid permanent suspension.',
             '{"KYC will be blocked","share the OTP","account suspension","keep account active"}', 69, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '40965a2f-e751-4b0f-b141-ce7dd7293c36', 'hi', 'cbi_impersonation', 'सीबीआई फर्जी कॉल — एफआईआर की धमकी', 'हम सीबीआई दिल्ली मुख्यालय से बोल रहे हैं। आपके नाम पर मनी लॉन्ड्रिंग केस में एफआईआर दर्ज हुई है। गिरफ्तारी से बचने के लिए तुरंत अपना बैंक खाता सत्यापित करें।',
             '{"एफआईआर दर्ज","मनी लॉन्ड्रिंग","तुरंत गिरफ्तारी","बैंक खाता सत्यापित"}', 131, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '3ddb7091-cf46-453d-b273-ccfec93de8a5', 'hi', 'digital_arrest', 'फर्जी सीबीआई डिजिटल गिरफ्तारी — पार्सल चेतावनी', 'मैं सीबीआई मुंबई से अधिकारी Iyer बोल रहा हूं। आपके आधार से जुड़े पार्सल में अवैध सामान मिला है। आप डिजिटल गिरफ्तारी में हैं। कॉल मत काटिए वरना गिरफ्तारी वारंट जारी होगा।',
             '{"डिजिटल गिरफ्तारी","कॉल मत काटिए","वारंट","आधार लिंक"}', 110, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             'd8e6a907-8e08-41c7-87ea-d460e0a55008', 'hi', 'digital_arrest', 'फर्जी सीबीआई डिजिटल गिरफ्तारी — पार्सल चेतावनी', 'मैं सीबीआई मुंबई से अधिकारी Iyer बोल रहा हूं। आपके आधार से जुड़े पार्सल में अवैध सामान मिला है। आप डिजिटल गिरफ्तारी में हैं। कॉल मत काटिए वरना गिरफ्तारी वारंट जारी होगा।',
             '{"डिजिटल गिरफ्तारी","कॉल मत काटिए","वारंट","आधार लिंक"}', 173, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '96880216-d581-476e-9cca-4fe1c8cb52c3', 'en', 'bank_kyc', 'Bank KYC Expiry Fraud', 'Dear customer, your bank account KYC will be blocked within 2 hours. Share the OTP sent to your phone immediately to keep your account active and avoid permanent suspension.',
             '{"KYC will be blocked","share the OTP","account suspension","keep account active"}', 170, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '2debbed7-b7ab-4020-8a69-99d7ae9bde30', 'en', 'customs_seizure', 'Customs Parcel Seizure Scam', 'This is customs department Mumbai airport. A parcel booked under your name has been seized, containing banned items and cash worth lakhs. Pay the customs penalty now to avoid FIR.',
             '{"parcel seized","customs penalty","banned items","pay now"}', 56, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '50e2912a-0d0c-4639-b756-ce4baa3089a4', 'en', 'tax_evasion', 'Income Tax Department Threat Call', 'This call is from the Income Tax Department, Investigation Wing. Discrepancies worth several lakhs have been found in your recent filings. A non-bailable warrant is being prepared unless you settle the pending dues today via UPI.',
             '{"income tax department","non-bailable warrant","settle dues","pay via UPI"}', 14, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '01716d7b-2bea-4456-9bbc-fe1c8dc97477', 'en', 'digital_arrest', 'Fake CBI Digital Arrest — Parcel Warning', 'This is Officer Verma from CBI Mumbai. Your Aadhaar-linked parcel containing illegal substances has been intercepted at customs. You are under digital arrest. Do not disconnect this call or contact anyone, or a warrant will be issued for your arrest.',
             '{"digital arrest","do not disconnect","warrant","aadhaar linked","customs intercepted"}', 77, TRUE
            );
INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '8d6e9d21-e0da-4da8-99e2-b95517358624', 'hi', 'cbi_impersonation', 'सीबीआई फर्जी कॉल — एफआईआर की धमकी', 'हम सीबीआई दिल्ली मुख्यालय से बोल रहे हैं। आपके नाम पर मनी लॉन्ड्रिंग केस में एफआईआर दर्ज हुई है। गिरफ्तारी से बचने के लिए तुरंत अपना बैंक खाता सत्यापित करें।',
             '{"एफआईआर दर्ज","मनी लॉन्ड्रिंग","तुरंत गिरफ्तारी","बैंक खाता सत्यापित"}', 35, TRUE
            );

-- note_verify.counterfeit_serials
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '1XK403507', 500, NOW() - interval '168 days',
             4, 'NCRP'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '9GH883301', 500, NOW() - interval '221 days',
             6, 'RBI Alert'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '9GH658453', 500, NOW() - interval '361 days',
             8, 'Bank Report'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '3AQ516359', 500, NOW() - interval '380 days',
             2, 'system'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '3AQ582087', 500, NOW() - interval '40 days',
             11, 'system'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '4LM524068', 500, NOW() - interval '364 days',
             21, 'system'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '1XK220768', 500, NOW() - interval '208 days',
             1, 'Bank Report'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '7CF940247', 500, NOW() - interval '317 days',
             15, 'Bank Report'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '3AQ557925', 2000, NOW() - interval '55 days',
             8, 'system'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '4LM519902', 2000, NOW() - interval '269 days',
             3, 'system'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '1XK882033', 2000, NOW() - interval '174 days',
             8, 'Bank Report'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '7CF180089', 2000, NOW() - interval '262 days',
             21, 'NCRP'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '4LM634723', 2000, NOW() - interval '100 days',
             25, 'Bank Report'
            );
INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '1XK862712', 2000, NOW() - interval '331 days',
             5, 'RBI Alert'
            );

-- fraud_graph.clusters
INSERT INTO fraud_graph.clusters
            (id, name, node_count, edge_count, estimated_loss, victim_count, status, detected_at)
            VALUES ('a2109d45-19bf-428b-999c-f2e324dd4145', 'Mumbai Digital Arrest Ring', 30, 55, 1271033.96,
             24, 'active',
             NOW() - interval '93 days');
INSERT INTO fraud_graph.clusters
            (id, name, node_count, edge_count, estimated_loss, victim_count, status, detected_at)
            VALUES ('0a9354af-c769-4d88-b5e7-23740b9e4164', 'Delhi CBI Impersonation Network', 30, 55, 5017992.39,
             56, 'dismantled',
             NOW() - interval '43 days');
INSERT INTO fraud_graph.clusters
            (id, name, node_count, edge_count, estimated_loss, victim_count, status, detected_at)
            VALUES ('1ee3fc18-41ab-4278-860d-4ed662ccc661', 'Hyderabad Customs Scam Cell', 30, 55, 1828595.97,
             57, 'dismantled',
             NOW() - interval '257 days');
INSERT INTO fraud_graph.clusters
            (id, name, node_count, edge_count, estimated_loss, victim_count, status, detected_at)
            VALUES ('5cf43a61-4444-463a-9dff-624e082b3e7f', 'Bangalore UPI Mule Network', 30, 55, 3979648.01,
             44, 'dismantled',
             NOW() - interval '234 days');

-- fraud_graph.entities
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('8c8f1ca5-2691-4ce1-8629-cb17d678f2f2', 'device', 'IMEI-823944932018331', 'IMEI-823944932018331', 80, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '329 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('84887935-a792-4449-ad9c-b28734cee04f', 'device', 'IMEI-455939518599648', 'IMEI-455939518599648', 49, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '235 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('6acd6c38-6af2-4922-91fb-82adcddbde6c', 'bank_account', '44905814770', '44905814770', 43, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '198 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('51b470f8-c190-4ada-87ca-13e1fb9002fe', 'phone_number', '+917387820537', '+917387820537', 79, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '314 days', NOW() - interval '8 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('22c61a62-eec6-477f-ac2f-cf6c83b9f228', 'bank_account', '98079359782', '98079359782', 43, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '240 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('e8ea141a-eace-4169-83af-fb5fac08bf55', 'person', 'Person_6626', 'Person_6626', 85, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '53 days', NOW() - interval '8 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('a7e02a2f-bdf6-410e-9b32-1e600340585d', 'upi_id', '1168114160@ybl', '1168114160@ybl', 68, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '278 days', NOW() - interval '8 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('c0cbf13f-dfce-4fb3-bbb0-42091aa431bc', 'upi_id', '6857897124@okhdfcbank', '6857897124@okhdfcbank', 64, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '219 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('1461b612-ba92-4ed0-8274-c82fae504048', 'upi_id', '2437308013@okhdfcbank', '2437308013@okhdfcbank', 46, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '295 days', NOW() - interval '10 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('0b95c3ea-92f8-47c7-85dc-371b43c8623f', 'bank_account', '49251925462', '49251925462', 78, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '372 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('0cfb3120-0a89-4b92-86ba-271c4f8b742b', 'bank_account', '65281685054', '65281685054', 51, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '119 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('6733c50e-dfe7-41c4-8975-371df1b68332', 'device', 'IMEI-316180677427278', 'IMEI-316180677427278', 54, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '80 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('c22116db-5a97-4d83-ae37-994f0c950ac0', 'phone_number', '+917434396266', '+917434396266', 72, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '286 days', NOW() - interval '8 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('b4c61d2a-ef2d-4672-a349-5614353ec2c4', 'phone_number', '+918446391956', '+918446391956', 96, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '326 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('fad7adc8-e90c-4999-b5b0-6fbe43f56cc0', 'upi_id', '1662510569@oksbi', '1662510569@oksbi', 93, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '364 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('5c673135-7878-4a96-9638-a2e1a0dbce7a', 'person', 'Person_3712', 'Person_3712', 86, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '234 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('b7433814-5681-46f9-8f51-0066ecae4a52', 'bank_account', '37947383473', '37947383473', 63, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '357 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('406600bf-8fc1-4d2c-844e-b539be46acf2', 'ip_address', '119.144.195.129', '119.144.195.129', 73, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '224 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('8c000cf8-863e-4827-a83c-3daeba511a8c', 'person', 'Person_3267', 'Person_3267', 95, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '138 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('7bfbbc93-0beb-456d-b48e-f10c950a1f5a', 'upi_id', '9049270990@paytm', '9049270990@paytm', 99, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '62 days', NOW() - interval '8 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('f4e33f34-a67f-463c-9724-50bbbf9a1cd8', 'device', 'IMEI-194434670273488', 'IMEI-194434670273488', 88, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '92 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('aea75690-69b4-4c84-b29e-224f5672f844', 'bank_account', '82613750606', '82613750606', 72, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '201 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('65af00c5-c021-4cb0-b3e1-11827b9bca95', 'bank_account', '15305152204', '15305152204', 98, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '251 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('4b7a4251-da29-40d4-960d-c695bd88c856', 'person', 'Person_8685', 'Person_8685', 68, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '325 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('04bbbfce-f53b-4876-a3ed-371bdded7f63', 'device', 'IMEI-388140847575124', 'IMEI-388140847575124', 53, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '86 days', NOW() - interval '8 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('d744c3b4-201b-41e7-8b9d-7b96b9697b72', 'device', 'IMEI-694219930456306', 'IMEI-694219930456306', 67, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '66 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('43418f58-4ebf-4afa-a9fb-73e368b80fd5', 'phone_number', '+917523334661', '+917523334661', 43, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '132 days', NOW() - interval '6 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('3c1ec779-514e-4af0-a740-d8b41e7baa3c', 'upi_id', '7969918312@okaxis', '7969918312@okaxis', 47, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '265 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('1ecdac39-8b10-4629-b1b9-677385d3cf75', 'upi_id', '3469810046@oksbi', '3469810046@oksbi', 58, '{}'::jsonb,
                 'a2109d45-19bf-428b-999c-f2e324dd4145', NOW() - interval '229 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('d1d04507-4d3c-4b4f-93d3-b9e0ea716ebd', 'bank_account', '96218518888', '96218518888', 75, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '20 days', NOW() - interval '6 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('c8c535da-9ad4-4c1d-8b5e-aa3da181aed4', 'device', 'IMEI-815700652282489', 'IMEI-815700652282489', 64, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '201 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('bde87935-08e3-4b96-a4ca-3fb874217012', 'person', 'Person_6850', 'Person_6850', 90, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '44 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('16503e2a-1a03-48ab-a0a4-21cd5dc9a677', 'phone_number', '+919822241896', '+919822241896', 80, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '63 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('68fe13a3-b058-4dec-9415-d5dbee685cb9', 'person', 'Person_6447', 'Person_6447', 48, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '32 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('8a6e742d-1818-4d9e-8013-bcd4177200a7', 'upi_id', '8281641403@oksbi', '8281641403@oksbi', 91, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '79 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('129adb44-c0b2-44eb-860e-2e6f616384b9', 'person', 'Person_8498', 'Person_8498', 42, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '160 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('4e0488be-17a0-4774-b5f4-ac7f57ae9470', 'phone_number', '+917856716405', '+917856716405', 96, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '31 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('df4b5f72-f2b3-40e4-9337-bb1f86058aea', 'device', 'IMEI-548362439519687', 'IMEI-548362439519687', 92, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '288 days', NOW() - interval '7 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('82d1a388-a107-4386-81e7-4e80f8bb0067', 'phone_number', '+919778416511', '+919778416511', 52, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '156 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('e513f62b-ba06-404f-b02f-cf3b67e6283a', 'device', 'IMEI-473716510704332', 'IMEI-473716510704332', 57, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '73 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('2b3e4659-7a01-44c1-8dae-8c280ae9ac57', 'bank_account', '67652775841', '67652775841', 86, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '227 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('5fe92520-b531-407a-944f-2255cbaaca7b', 'bank_account', '28451154479', '28451154479', 85, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '228 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('09ba0704-e084-4e2e-9490-0ecc9def9b7b', 'upi_id', '6804850108@okaxis', '6804850108@okaxis', 86, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '190 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('8b47adf6-bfca-43f7-b8fc-e2119b28f63d', 'ip_address', '71.29.38.172', '71.29.38.172', 80, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '217 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('b9eeda0a-bb63-49e1-821b-22c0a12a013c', 'upi_id', '1133747952@paytm', '1133747952@paytm', 83, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '234 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('1fd47cfe-f8c3-4ea2-980e-bf7514ac5e9c', 'phone_number', '+918013592436', '+918013592436', 89, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '340 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('7de42cab-f048-47bd-89b0-ab5604cab39f', 'bank_account', '90927557192', '90927557192', 73, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '197 days', NOW() - interval '6 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('9a3bcf18-ee8c-4dc0-8ad4-3408785b4c22', 'bank_account', '43102786814', '43102786814', 89, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '143 days', NOW() - interval '7 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('97bc3b7d-225d-4343-a320-139b1f7d3b19', 'phone_number', '+919627992499', '+919627992499', 58, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '365 days', NOW() - interval '7 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('19ee01c5-2fcc-4d8a-9b1c-d71b0ddea7db', 'phone_number', '+917582949109', '+917582949109', 94, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '47 days', NOW() - interval '7 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('49059f98-f464-499a-9f9e-5604108027ae', 'phone_number', '+918911737999', '+918911737999', 45, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '359 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('0a6457b4-a7a1-482e-9a8e-a599c986469b', 'upi_id', '4047453184@paytm', '4047453184@paytm', 74, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '158 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('bf34659a-0644-4929-8d17-452df2a70dfd', 'device', 'IMEI-898897039023876', 'IMEI-898897039023876', 99, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '368 days', NOW() - interval '10 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('0adcebcc-d7dc-42d5-8851-1353964f611e', 'phone_number', '+918552597094', '+918552597094', 72, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '124 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('bf60fb3a-3b37-4256-b7d6-6491bf800f0d', 'ip_address', '203.71.121.203', '203.71.121.203', 71, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '23 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('c8a2fc3a-14e5-4916-a455-05cb605dc540', 'upi_id', '6879428703@paytm', '6879428703@paytm', 48, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '323 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('425e3c57-320a-4d83-a0cc-208064db5786', 'phone_number', '+918710084067', '+918710084067', 85, '{}'::jsonb,
                 '0a9354af-c769-4d88-b5e7-23740b9e4164', NOW() - interval '378 days', NOW() - interval '7 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('e9067e16-7368-459d-ac9f-bc21dff20791', 'bank_account', '69125177852', '69125177852', 96, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '292 days', NOW() - interval '10 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('1a58ccc8-0ac1-4bc4-8f84-ff79ff4073f3', 'upi_id', '5849159641@paytm', '5849159641@paytm', 98, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '38 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('b5338512-5745-4680-be80-d3f9ac9322a0', 'upi_id', '2306204982@oksbi', '2306204982@oksbi', 60, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '373 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('7e45636b-10dd-41cf-9664-aea86712fe21', 'bank_account', '84143842498', '84143842498', 45, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '267 days', NOW() - interval '10 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('9e7f82dc-3a0f-40f1-b34a-bd7b3d0147e6', 'phone_number', '+919493857758', '+919493857758', 49, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '97 days', NOW() - interval '10 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('e50db8f6-0a23-4c78-9a2a-bf0951a259db', 'upi_id', '4709911999@okaxis', '4709911999@okaxis', 42, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '338 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('0ac06981-2709-4295-a746-a7904938d7fe', 'phone_number', '+917905415100', '+917905415100', 89, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '302 days', NOW() - interval '6 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('5108d8cd-1406-4580-b094-9f8d02e0ccdb', 'upi_id', '5425044246@paytm', '5425044246@paytm', 58, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '338 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('f8592779-aaef-4965-85e7-6cadce0115ba', 'bank_account', '64710276773', '64710276773', 61, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '320 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('9ec64938-e4b0-49fa-9c47-e4d14701fc59', 'bank_account', '55625881537', '55625881537', 47, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '146 days', NOW() - interval '7 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('e47f1f26-cfc6-49d0-aac1-dbc9b8a8e528', 'phone_number', '+917415802902', '+917415802902', 43, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '158 days', NOW() - interval '6 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('f4e54e0c-e323-4cd7-9a4e-fc0dd3b9026d', 'device', 'IMEI-379526857433315', 'IMEI-379526857433315', 95, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '91 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('437ee980-5602-4683-8d3c-93959d21e09c', 'device', 'IMEI-452087336279935', 'IMEI-452087336279935', 52, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '400 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('4f7e2c5b-93f5-48f7-bcbc-69df0d427433', 'bank_account', '87747016873', '87747016873', 53, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '308 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('d32d4ae7-05af-4479-afaa-a51b1189842d', 'phone_number', '+918208416260', '+918208416260', 71, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '315 days', NOW() - interval '10 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('7d2bdda8-38e8-4339-a7d0-a3ef694f519e', 'upi_id', '5756663747@oksbi', '5756663747@oksbi', 96, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '145 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('7fd97fca-c7d9-4fd4-ad6d-699f4f0cddbc', 'person', 'Person_6995', 'Person_6995', 42, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '215 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('54d62db7-2af4-444f-a83f-f664124ca252', 'upi_id', '6131005449@paytm', '6131005449@paytm', 58, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '47 days', NOW() - interval '6 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('b1cdc6d4-5382-4628-a137-7250fc5b482c', 'upi_id', '1510289448@okaxis', '1510289448@okaxis', 65, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '201 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('0b328c4b-fecb-40f9-b76d-5b2abd33546b', 'upi_id', '1619623590@paytm', '1619623590@paytm', 72, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '215 days', NOW() - interval '8 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('9b4c109d-36ae-43b3-a553-1667ea131ae5', 'phone_number', '+917167134213', '+917167134213', 48, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '375 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('28057f03-f016-44d3-8f3a-33db25f272cc', 'person', 'Person_9508', 'Person_9508', 69, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '86 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('9b5118de-22be-43b2-ac26-5849b30678c0', 'device', 'IMEI-469256118661083', 'IMEI-469256118661083', 99, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '323 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('1758a1da-5c6e-4fba-a0ce-77f7216f3167', 'phone_number', '+919647849438', '+919647849438', 87, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '163 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('900d7239-8f6b-4c18-9ae4-c8cb6fda1c0b', 'bank_account', '88794705516', '88794705516', 77, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '167 days', NOW() - interval '10 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('1cfbccbd-a228-484b-a6ac-6f17b3655100', 'phone_number', '+919038349447', '+919038349447', 56, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '345 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('f7d45c99-7fe5-4c94-b453-7854c78d65ac', 'upi_id', '4098389895@paytm', '4098389895@paytm', 70, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '97 days', NOW() - interval '8 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('3aa86899-41f4-48bc-9aba-dacf52c5d1e8', 'upi_id', '8907752604@oksbi', '8907752604@oksbi', 92, '{}'::jsonb,
                 '1ee3fc18-41ab-4278-860d-4ed662ccc661', NOW() - interval '358 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('1b0d5630-551e-48c9-b0e1-a0a8958d5bba', 'upi_id', '4008714405@oksbi', '4008714405@oksbi', 41, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '235 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('25a3479f-0597-46f4-89c5-666108cfba65', 'bank_account', '63689702838', '63689702838', 60, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '349 days', NOW() - interval '7 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('4ac22938-0413-4fea-aa04-1c47fb6b6a1c', 'upi_id', '6038780151@paytm', '6038780151@paytm', 61, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '289 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('5f772a17-f7f5-45cd-a1d7-d85d994ea666', 'upi_id', '3079537716@oksbi', '3079537716@oksbi', 57, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '295 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('bc8f19ac-6d56-444d-9c70-a050fe0cbaa9', 'phone_number', '+918278244804', '+918278244804', 89, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '157 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('f78481ca-a8ae-449c-871c-157473b44be7', 'upi_id', '7395219544@ybl', '7395219544@ybl', 62, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '296 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('c6ee2223-b96c-40af-b17b-23c1786a40cf', 'phone_number', '+919463064097', '+919463064097', 83, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '288 days', NOW() - interval '6 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('238e4285-9571-4b3b-a192-fbc4a715790a', 'device', 'IMEI-427019439027605', 'IMEI-427019439027605', 42, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '157 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('8b086099-5521-466a-902a-3c87e839cdd8', 'bank_account', '74733848421', '74733848421', 79, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '389 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('ac642857-6013-45c4-8ea6-c7ae64b4b271', 'phone_number', '+917218035843', '+917218035843', 82, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '281 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('461393fa-eff7-4a51-b018-619964e962e7', 'upi_id', '1225447588@ybl', '1225447588@ybl', 61, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '377 days', NOW() - interval '7 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('7de08716-7100-4055-98b8-1b706b7bafb0', 'phone_number', '+917590416424', '+917590416424', 40, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '291 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('cbaee268-8fac-4cc0-9b6e-54ae42d025a4', 'bank_account', '77345401938', '77345401938', 87, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '380 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('ed5b9337-a5d8-40ae-a4f3-6faf89159c53', 'device', 'IMEI-570497239305119', 'IMEI-570497239305119', 96, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '100 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('6a5d2fe7-78e6-4001-b3e2-0ca03b7332b6', 'ip_address', '102.253.95.240', '102.253.95.240', 87, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '158 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('79ddffc9-9c15-444b-bf2d-3e0b5dad02f4', 'phone_number', '+919439377645', '+919439377645', 78, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '64 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('a76f1d08-5697-4bea-830d-0b2960bc22e9', 'phone_number', '+919754415831', '+919754415831', 74, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '278 days', NOW() - interval '7 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('be96fae5-420e-4a90-8018-d048622bbbe5', 'device', 'IMEI-626943113188600', 'IMEI-626943113188600', 57, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '108 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('f5c51b83-3838-48fe-b1f8-919459681d42', 'bank_account', '74205493296', '74205493296', 92, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '228 days', NOW() - interval '8 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('c8bedcce-c8db-4e15-a9f1-cc3355093ee6', 'bank_account', '61227530463', '61227530463', 68, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '395 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('1fdfe259-8382-4714-bd12-e4a9c9d32007', 'ip_address', '78.5.133.168', '78.5.133.168', 63, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '364 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('c61620b7-834b-4831-bfe2-189fd64e710a', 'phone_number', '+917507771858', '+917507771858', 69, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '167 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('a7567274-9370-41c0-9af1-765e783e9c48', 'bank_account', '84145933272', '84145933272', 69, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '392 days', NOW() - interval '9 days');
INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('d784ba7e-9706-43a4-935b-9b953787be18', 'bank_account', '87833918785', '87833918785', 44, '{}'::jsonb,
                 '5cf43a61-4444-463a-9dff-624e082b3e7f', NOW() - interval '298 days', NOW() - interval '1 days');

-- fraud_graph.edges
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('10688484-4cbd-4758-b528-ce8b2a0803ac', '43418f58-4ebf-4afa-a9fb-73e368b80fd5', '406600bf-8fc1-4d2c-844e-b539be46acf2', 'owns_account', 14.74, '{}'::jsonb,
                 NOW() - interval '77 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('b0039d06-5a7c-4c10-9e73-62658d676657', '0cfb3120-0a89-4b92-86ba-271c4f8b742b', '3c1ec779-514e-4af0-a740-d8b41e7baa3c', 'linked_to', 3.79, '{}'::jsonb,
                 NOW() - interval '106 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('bfe14ca1-a63f-486e-8bf9-1fd1462e4879', '8c000cf8-863e-4827-a83c-3daeba511a8c', '5c673135-7878-4a96-9638-a2e1a0dbce7a', 'transferred_to', 22.57, '{}'::jsonb,
                 NOW() - interval '229 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('b650c155-70e7-48e3-9173-19729086dd7f', 'fad7adc8-e90c-4999-b5b0-6fbe43f56cc0', '22c61a62-eec6-477f-ac2f-cf6c83b9f228', 'reported_by', 11.96, '{}'::jsonb,
                 NOW() - interval '30 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('49bacd2b-e850-4f5d-81b7-f12f34ad8725', 'fad7adc8-e90c-4999-b5b0-6fbe43f56cc0', 'aea75690-69b4-4c84-b29e-224f5672f844', 'uses_device', 18.36, '{}'::jsonb,
                 NOW() - interval '203 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('80488a41-bf1a-4fcc-83fc-1e3a0243a71c', '43418f58-4ebf-4afa-a9fb-73e368b80fd5', '8c8f1ca5-2691-4ce1-8629-cb17d678f2f2', 'owns_account', 14.88, '{}'::jsonb,
                 NOW() - interval '24 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('615e60ad-2747-45af-8049-c0a3f6e05ee7', '6733c50e-dfe7-41c4-8975-371df1b68332', '65af00c5-c021-4cb0-b3e1-11827b9bca95', 'transferred_to', 13.99, '{}'::jsonb,
                 NOW() - interval '31 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('10c9e7c5-966a-44db-a048-9137321a5031', '5c673135-7878-4a96-9638-a2e1a0dbce7a', '84887935-a792-4449-ad9c-b28734cee04f', 'uses_device', 10.81, '{}'::jsonb,
                 NOW() - interval '70 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('d2d02441-301c-49ae-b05a-fb4cadec679e', '4b7a4251-da29-40d4-960d-c695bd88c856', 'f4e33f34-a67f-463c-9724-50bbbf9a1cd8', 'reported_by', 9.99, '{}'::jsonb,
                 NOW() - interval '196 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('7e23179a-9149-46fe-b24b-1cf809d35764', '3c1ec779-514e-4af0-a740-d8b41e7baa3c', 'c22116db-5a97-4d83-ae37-994f0c950ac0', 'reported_by', 2.93, '{}'::jsonb,
                 NOW() - interval '277 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('334c6b67-2ead-4251-acd3-7e5a1f188fe2', 'f4e33f34-a67f-463c-9724-50bbbf9a1cd8', '3c1ec779-514e-4af0-a740-d8b41e7baa3c', 'connected_from', 3.85, '{}'::jsonb,
                 NOW() - interval '276 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('386df011-0556-4f52-8db6-2684c76bf793', 'b7433814-5681-46f9-8f51-0066ecae4a52', '22c61a62-eec6-477f-ac2f-cf6c83b9f228', 'owns_account', 21.04, '{}'::jsonb,
                 NOW() - interval '12 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('f0471d80-8536-45b9-a0cd-acd736bf7ce4', 'fad7adc8-e90c-4999-b5b0-6fbe43f56cc0', 'aea75690-69b4-4c84-b29e-224f5672f844', 'reported_by', 13.77, '{}'::jsonb,
                 NOW() - interval '118 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('60f9a015-4f51-48ca-993f-a5fd1a98ee6f', 'fad7adc8-e90c-4999-b5b0-6fbe43f56cc0', '6733c50e-dfe7-41c4-8975-371df1b68332', 'uses_number', 7.62, '{}'::jsonb,
                 NOW() - interval '58 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('892f864d-e794-4bef-bea4-b33491a88774', 'd744c3b4-201b-41e7-8b9d-7b96b9697b72', 'aea75690-69b4-4c84-b29e-224f5672f844', 'reported_by', 15.76, '{}'::jsonb,
                 NOW() - interval '9 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('6556473c-403f-42e9-8b52-7ace2847434e', 'a7e02a2f-bdf6-410e-9b32-1e600340585d', '6acd6c38-6af2-4922-91fb-82adcddbde6c', 'transferred_to', 15.25, '{}'::jsonb,
                 NOW() - interval '229 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('39748bd3-d130-4fd3-8515-7d91e7d9a8ab', 'aea75690-69b4-4c84-b29e-224f5672f844', '65af00c5-c021-4cb0-b3e1-11827b9bca95', 'called', 6.87, '{}'::jsonb,
                 NOW() - interval '23 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('fa5da36d-4c46-4d43-8199-bd04fd31262a', 'fad7adc8-e90c-4999-b5b0-6fbe43f56cc0', 'c0cbf13f-dfce-4fb3-bbb0-42091aa431bc', 'owns_account', 19.11, '{}'::jsonb,
                 NOW() - interval '29 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('3dcffbd1-5e46-4ab1-9860-929ea204575f', 'b7433814-5681-46f9-8f51-0066ecae4a52', '0b95c3ea-92f8-47c7-85dc-371b43c8623f', 'owns_account', 20.58, '{}'::jsonb,
                 NOW() - interval '295 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('90666c97-8728-49e0-b85f-f1e0c3fd376d', '8c000cf8-863e-4827-a83c-3daeba511a8c', '7bfbbc93-0beb-456d-b48e-f10c950a1f5a', 'connected_from', 6.69, '{}'::jsonb,
                 NOW() - interval '74 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('4fbd11cc-a30e-4e33-a127-90a00b55848e', 'b7433814-5681-46f9-8f51-0066ecae4a52', 'c0cbf13f-dfce-4fb3-bbb0-42091aa431bc', 'reported_by', 8.21, '{}'::jsonb,
                 NOW() - interval '32 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('8c55e739-9365-4e83-936a-5e3004ccf063', '8c000cf8-863e-4827-a83c-3daeba511a8c', '1ecdac39-8b10-4629-b1b9-677385d3cf75', 'uses_number', 16.02, '{}'::jsonb,
                 NOW() - interval '219 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('5392cb17-6696-4e30-8e20-f18a1c03b582', '5c673135-7878-4a96-9638-a2e1a0dbce7a', '84887935-a792-4449-ad9c-b28734cee04f', 'connected_from', 23.60, '{}'::jsonb,
                 NOW() - interval '196 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('02793756-d6e5-492f-b2d7-f368228fb95f', '0cfb3120-0a89-4b92-86ba-271c4f8b742b', '65af00c5-c021-4cb0-b3e1-11827b9bca95', 'reported_by', 10.80, '{}'::jsonb,
                 NOW() - interval '154 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ea1fbc50-0e70-46f4-8dcd-88ab673e9f11', 'e8ea141a-eace-4169-83af-fb5fac08bf55', '04bbbfce-f53b-4876-a3ed-371bdded7f63', 'linked_to', 6.78, '{}'::jsonb,
                 NOW() - interval '116 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('51c0b4cc-df65-4237-9c9a-a56754a529db', '3c1ec779-514e-4af0-a740-d8b41e7baa3c', '65af00c5-c021-4cb0-b3e1-11827b9bca95', 'uses_number', 20.34, '{}'::jsonb,
                 NOW() - interval '30 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('7eb8e4cd-ea01-48e2-aa81-720b51dd3709', 'b4c61d2a-ef2d-4672-a349-5614353ec2c4', '406600bf-8fc1-4d2c-844e-b539be46acf2', 'uses_number', 10.32, '{}'::jsonb,
                 NOW() - interval '131 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('f71f3108-7a82-4144-9fd7-67164190ab2b', '0cfb3120-0a89-4b92-86ba-271c4f8b742b', 'f4e33f34-a67f-463c-9724-50bbbf9a1cd8', 'transferred_to', 23.13, '{}'::jsonb,
                 NOW() - interval '190 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('62ff6abd-8525-471c-9b3c-a3c17bd86406', '406600bf-8fc1-4d2c-844e-b539be46acf2', '4b7a4251-da29-40d4-960d-c695bd88c856', 'owns_account', 2.24, '{}'::jsonb,
                 NOW() - interval '194 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('6b8c89f7-28af-4655-a872-8d7b5ff22a56', '7bfbbc93-0beb-456d-b48e-f10c950a1f5a', '84887935-a792-4449-ad9c-b28734cee04f', 'transferred_to', 5.52, '{}'::jsonb,
                 NOW() - interval '287 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('f6f3cf2f-2b84-4f18-8e7b-e74b60ff9989', '5c673135-7878-4a96-9638-a2e1a0dbce7a', 'a7e02a2f-bdf6-410e-9b32-1e600340585d', 'connected_from', 8.28, '{}'::jsonb,
                 NOW() - interval '8 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('12c67b3e-6970-43e8-bac5-1fd9633d718a', 'a7e02a2f-bdf6-410e-9b32-1e600340585d', '4b7a4251-da29-40d4-960d-c695bd88c856', 'transferred_to', 18.93, '{}'::jsonb,
                 NOW() - interval '246 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('bb064af0-8cf9-41dc-a4c4-5aff5c8e016a', '65af00c5-c021-4cb0-b3e1-11827b9bca95', '7bfbbc93-0beb-456d-b48e-f10c950a1f5a', 'owns_account', 10.52, '{}'::jsonb,
                 NOW() - interval '123 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('cc713bb1-127e-4c35-90ec-02f64aa34114', '0cfb3120-0a89-4b92-86ba-271c4f8b742b', '04bbbfce-f53b-4876-a3ed-371bdded7f63', 'uses_device', 10.14, '{}'::jsonb,
                 NOW() - interval '274 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('f13c3366-beb4-4369-afb6-04b13ca39f81', '6733c50e-dfe7-41c4-8975-371df1b68332', '0b95c3ea-92f8-47c7-85dc-371b43c8623f', 'uses_device', 9.63, '{}'::jsonb,
                 NOW() - interval '255 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ff123183-6513-40d6-be2c-1d59b1c2681a', '51b470f8-c190-4ada-87ca-13e1fb9002fe', 'd744c3b4-201b-41e7-8b9d-7b96b9697b72', 'linked_to', 19.28, '{}'::jsonb,
                 NOW() - interval '164 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('6f7ec978-f9ba-42ad-9902-3386f6fed6bb', '6733c50e-dfe7-41c4-8975-371df1b68332', '0cfb3120-0a89-4b92-86ba-271c4f8b742b', 'reported_by', 2.10, '{}'::jsonb,
                 NOW() - interval '114 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('10a5500f-620d-401a-9649-ea2909a24c40', '22c61a62-eec6-477f-ac2f-cf6c83b9f228', '8c8f1ca5-2691-4ce1-8629-cb17d678f2f2', 'uses_device', 14.28, '{}'::jsonb,
                 NOW() - interval '300 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('28b2efaa-8216-4a52-89ef-380a22d8f031', '4b7a4251-da29-40d4-960d-c695bd88c856', 'b4c61d2a-ef2d-4672-a349-5614353ec2c4', 'uses_device', 4.66, '{}'::jsonb,
                 NOW() - interval '169 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('3e8c9f26-b8dc-4688-b4f4-c62c0b401d74', 'c22116db-5a97-4d83-ae37-994f0c950ac0', '8c000cf8-863e-4827-a83c-3daeba511a8c', 'owns_account', 12.98, '{}'::jsonb,
                 NOW() - interval '173 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('630ee01a-4e1a-42d8-916a-f7f627507cce', '04bbbfce-f53b-4876-a3ed-371bdded7f63', '43418f58-4ebf-4afa-a9fb-73e368b80fd5', 'linked_to', 24.20, '{}'::jsonb,
                 NOW() - interval '252 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('dd8d42fa-a4ef-42c9-ad3e-30157e2ff579', 'e8ea141a-eace-4169-83af-fb5fac08bf55', '4b7a4251-da29-40d4-960d-c695bd88c856', 'connected_from', 5.06, '{}'::jsonb,
                 NOW() - interval '280 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('77e882d1-65cf-4367-8e40-72362c4639ef', 'e8ea141a-eace-4169-83af-fb5fac08bf55', '1ecdac39-8b10-4629-b1b9-677385d3cf75', 'called', 13.57, '{}'::jsonb,
                 NOW() - interval '39 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('fcc590d1-088a-42c2-bd65-c5364567120e', '84887935-a792-4449-ad9c-b28734cee04f', '04bbbfce-f53b-4876-a3ed-371bdded7f63', 'called', 10.90, '{}'::jsonb,
                 NOW() - interval '119 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('a995f931-b4d2-4ad8-81f6-dd646130a4eb', '65af00c5-c021-4cb0-b3e1-11827b9bca95', '22c61a62-eec6-477f-ac2f-cf6c83b9f228', 'called', 6.25, '{}'::jsonb,
                 NOW() - interval '234 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('fc284fc3-e99d-4462-8ccb-d16bba9defa9', '84887935-a792-4449-ad9c-b28734cee04f', '7bfbbc93-0beb-456d-b48e-f10c950a1f5a', 'linked_to', 16.82, '{}'::jsonb,
                 NOW() - interval '9 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('8c85152b-1fda-480b-9561-41dde21af751', '406600bf-8fc1-4d2c-844e-b539be46acf2', 'b4c61d2a-ef2d-4672-a349-5614353ec2c4', 'called', 1.40, '{}'::jsonb,
                 NOW() - interval '141 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('d09b68c9-8a92-4256-b6f6-72c822664583', '0b95c3ea-92f8-47c7-85dc-371b43c8623f', '8c8f1ca5-2691-4ce1-8629-cb17d678f2f2', 'reported_by', 20.35, '{}'::jsonb,
                 NOW() - interval '92 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('5e3727c3-6ad2-49bb-b226-e596c41633b3', '51b470f8-c190-4ada-87ca-13e1fb9002fe', 'b7433814-5681-46f9-8f51-0066ecae4a52', 'uses_number', 6.78, '{}'::jsonb,
                 NOW() - interval '270 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('98158b8d-989a-47d4-a801-879d97ad44c5', '43418f58-4ebf-4afa-a9fb-73e368b80fd5', '6733c50e-dfe7-41c4-8975-371df1b68332', 'uses_device', 20.08, '{}'::jsonb,
                 NOW() - interval '41 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('2ee2696f-22b6-4f65-8238-15c865f586f7', '8b47adf6-bfca-43f7-b8fc-e2119b28f63d', '9a3bcf18-ee8c-4dc0-8ad4-3408785b4c22', 'owns_account', 24.77, '{}'::jsonb,
                 NOW() - interval '116 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('306da66a-3ecc-4514-8dfa-588c15c7b912', '49059f98-f464-499a-9f9e-5604108027ae', 'c8a2fc3a-14e5-4916-a455-05cb605dc540', 'transferred_to', 16.69, '{}'::jsonb,
                 NOW() - interval '17 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('3af661f5-11af-4b35-859f-0bf195856fff', '5fe92520-b531-407a-944f-2255cbaaca7b', '7de42cab-f048-47bd-89b0-ab5604cab39f', 'linked_to', 2.35, '{}'::jsonb,
                 NOW() - interval '5 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('71a7af44-3ada-4ebf-8f88-3312394f72c8', '8a6e742d-1818-4d9e-8013-bcd4177200a7', 'bde87935-08e3-4b96-a4ca-3fb874217012', 'linked_to', 21.29, '{}'::jsonb,
                 NOW() - interval '170 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('412d992f-d96f-4d0e-99a3-f4d488317c36', '425e3c57-320a-4d83-a0cc-208064db5786', '16503e2a-1a03-48ab-a0a4-21cd5dc9a677', 'called', 6.51, '{}'::jsonb,
                 NOW() - interval '291 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('098e5044-342e-4a0e-9348-7b0a022af132', 'df4b5f72-f2b3-40e4-9337-bb1f86058aea', 'c8c535da-9ad4-4c1d-8b5e-aa3da181aed4', 'transferred_to', 17.43, '{}'::jsonb,
                 NOW() - interval '144 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('41783742-d1ba-4591-9914-4e37f13c42f4', '9a3bcf18-ee8c-4dc0-8ad4-3408785b4c22', '49059f98-f464-499a-9f9e-5604108027ae', 'called', 5.30, '{}'::jsonb,
                 NOW() - interval '162 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('9a3f02fb-b1bb-4a48-bf10-32586ac9a770', '129adb44-c0b2-44eb-860e-2e6f616384b9', '9a3bcf18-ee8c-4dc0-8ad4-3408785b4c22', 'uses_number', 19.05, '{}'::jsonb,
                 NOW() - interval '204 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('29f40aab-9ef1-411a-8a2e-705497b044d3', '82d1a388-a107-4386-81e7-4e80f8bb0067', '8a6e742d-1818-4d9e-8013-bcd4177200a7', 'owns_account', 14.60, '{}'::jsonb,
                 NOW() - interval '200 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('bd0c0581-d334-4051-a563-cd7ceae551f9', '7de42cab-f048-47bd-89b0-ab5604cab39f', 'e513f62b-ba06-404f-b02f-cf3b67e6283a', 'reported_by', 19.13, '{}'::jsonb,
                 NOW() - interval '72 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('f5f795e6-b324-4dcb-be13-3cb11ac3b33c', 'bf34659a-0644-4929-8d17-452df2a70dfd', 'bde87935-08e3-4b96-a4ca-3fb874217012', 'connected_from', 2.29, '{}'::jsonb,
                 NOW() - interval '224 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('99266241-21bf-4dc6-954b-cd4fc09e80b8', 'c8a2fc3a-14e5-4916-a455-05cb605dc540', 'bde87935-08e3-4b96-a4ca-3fb874217012', 'connected_from', 15.52, '{}'::jsonb,
                 NOW() - interval '204 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('f2404fd1-3501-4941-8787-fe6f4ccdcb02', 'd1d04507-4d3c-4b4f-93d3-b9e0ea716ebd', '19ee01c5-2fcc-4d8a-9b1c-d71b0ddea7db', 'uses_device', 19.81, '{}'::jsonb,
                 NOW() - interval '231 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('82c0202a-8c6c-4393-a191-fb7e67afd639', '4e0488be-17a0-4774-b5f4-ac7f57ae9470', '2b3e4659-7a01-44c1-8dae-8c280ae9ac57', 'reported_by', 11.36, '{}'::jsonb,
                 NOW() - interval '300 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('5d540f44-180e-4ed9-abab-85c65aabfe41', '5fe92520-b531-407a-944f-2255cbaaca7b', 'bde87935-08e3-4b96-a4ca-3fb874217012', 'uses_device', 20.15, '{}'::jsonb,
                 NOW() - interval '38 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('470ff1db-0bf3-406b-b5b9-acdc8e2f7f69', 'df4b5f72-f2b3-40e4-9337-bb1f86058aea', '68fe13a3-b058-4dec-9415-d5dbee685cb9', 'reported_by', 18.08, '{}'::jsonb,
                 NOW() - interval '79 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('4ec6e16f-6bcb-4af2-850c-2f7233fac59c', '5fe92520-b531-407a-944f-2255cbaaca7b', 'e513f62b-ba06-404f-b02f-cf3b67e6283a', 'connected_from', 3.56, '{}'::jsonb,
                 NOW() - interval '3 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('83686622-f745-4505-9a1b-51d3cccaabdb', '8b47adf6-bfca-43f7-b8fc-e2119b28f63d', '2b3e4659-7a01-44c1-8dae-8c280ae9ac57', 'uses_device', 3.45, '{}'::jsonb,
                 NOW() - interval '45 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('428a3849-e901-44f6-a925-df1c20343e51', '09ba0704-e084-4e2e-9490-0ecc9def9b7b', '8b47adf6-bfca-43f7-b8fc-e2119b28f63d', 'reported_by', 3.48, '{}'::jsonb,
                 NOW() - interval '46 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('5040d235-58da-41c9-820c-ace579736c57', '7de42cab-f048-47bd-89b0-ab5604cab39f', 'bde87935-08e3-4b96-a4ca-3fb874217012', 'connected_from', 21.73, '{}'::jsonb,
                 NOW() - interval '7 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('6ff482ea-9d47-4653-a60a-b1bfe825cb61', '09ba0704-e084-4e2e-9490-0ecc9def9b7b', '5fe92520-b531-407a-944f-2255cbaaca7b', 'transferred_to', 18.40, '{}'::jsonb,
                 NOW() - interval '287 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ebe51208-ad5a-4208-863d-4ca8c4fcde79', '9a3bcf18-ee8c-4dc0-8ad4-3408785b4c22', '1fd47cfe-f8c3-4ea2-980e-bf7514ac5e9c', 'uses_number', 17.45, '{}'::jsonb,
                 NOW() - interval '87 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('e51d1ef4-e87a-40ab-8ef0-8571ae169f48', 'df4b5f72-f2b3-40e4-9337-bb1f86058aea', '82d1a388-a107-4386-81e7-4e80f8bb0067', 'uses_device', 12.83, '{}'::jsonb,
                 NOW() - interval '33 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('802dea5c-ec48-4da4-9655-7a6ee148d71b', '09ba0704-e084-4e2e-9490-0ecc9def9b7b', 'df4b5f72-f2b3-40e4-9337-bb1f86058aea', 'reported_by', 8.19, '{}'::jsonb,
                 NOW() - interval '40 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('cae4c6ba-837c-4cc9-bf5a-d91ea2698535', 'df4b5f72-f2b3-40e4-9337-bb1f86058aea', '4e0488be-17a0-4774-b5f4-ac7f57ae9470', 'linked_to', 15.25, '{}'::jsonb,
                 NOW() - interval '101 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('4a16f3b8-b14d-4b4c-b0b5-71b96df947d1', '16503e2a-1a03-48ab-a0a4-21cd5dc9a677', '68fe13a3-b058-4dec-9415-d5dbee685cb9', 'uses_device', 1.16, '{}'::jsonb,
                 NOW() - interval '203 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('99451669-5669-41ab-b820-83d1b9246652', 'c8a2fc3a-14e5-4916-a455-05cb605dc540', '97bc3b7d-225d-4343-a320-139b1f7d3b19', 'reported_by', 20.30, '{}'::jsonb,
                 NOW() - interval '169 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('4ccd16c2-edc3-49c8-81ba-31dac74cf02a', 'e513f62b-ba06-404f-b02f-cf3b67e6283a', '09ba0704-e084-4e2e-9490-0ecc9def9b7b', 'uses_number', 8.21, '{}'::jsonb,
                 NOW() - interval '103 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('2d294c6e-b667-4ffa-a2fe-b98b6b4d625c', 'e513f62b-ba06-404f-b02f-cf3b67e6283a', '8a6e742d-1818-4d9e-8013-bcd4177200a7', 'reported_by', 24.25, '{}'::jsonb,
                 NOW() - interval '150 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('2acb2e1b-efd3-4a3d-bc6d-9e60ce9b4ad7', '0a6457b4-a7a1-482e-9a8e-a599c986469b', '19ee01c5-2fcc-4d8a-9b1c-d71b0ddea7db', 'linked_to', 24.23, '{}'::jsonb,
                 NOW() - interval '125 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('43532f26-3a85-4b95-a519-cae593cef76e', '5fe92520-b531-407a-944f-2255cbaaca7b', 'df4b5f72-f2b3-40e4-9337-bb1f86058aea', 'reported_by', 9.76, '{}'::jsonb,
                 NOW() - interval '289 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('0bb51106-0dda-4a7e-8298-0477bbe2d7da', '9a3bcf18-ee8c-4dc0-8ad4-3408785b4c22', '7de42cab-f048-47bd-89b0-ab5604cab39f', 'uses_number', 17.36, '{}'::jsonb,
                 NOW() - interval '282 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('4c0fe78a-40b0-43a3-a986-792442f9eeeb', 'bf34659a-0644-4929-8d17-452df2a70dfd', '8b47adf6-bfca-43f7-b8fc-e2119b28f63d', 'owns_account', 11.52, '{}'::jsonb,
                 NOW() - interval '150 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('131f5d83-d503-4e54-afff-04f84b71b3b1', 'bde87935-08e3-4b96-a4ca-3fb874217012', 'c8a2fc3a-14e5-4916-a455-05cb605dc540', 'reported_by', 17.15, '{}'::jsonb,
                 NOW() - interval '72 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('657cd282-373d-4202-8c81-6eba1e05bb7f', '82d1a388-a107-4386-81e7-4e80f8bb0067', '4e0488be-17a0-4774-b5f4-ac7f57ae9470', 'uses_device', 16.81, '{}'::jsonb,
                 NOW() - interval '217 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('f4675f4a-9abe-45f0-8575-d1f33a6a41f0', 'bde87935-08e3-4b96-a4ca-3fb874217012', '8b47adf6-bfca-43f7-b8fc-e2119b28f63d', 'linked_to', 14.97, '{}'::jsonb,
                 NOW() - interval '274 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('62deca4f-7c5a-413b-b643-8506c5807f0a', '425e3c57-320a-4d83-a0cc-208064db5786', '0a6457b4-a7a1-482e-9a8e-a599c986469b', 'reported_by', 14.05, '{}'::jsonb,
                 NOW() - interval '185 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('0cd80f85-003e-4b08-9a9e-5cfb4770db40', 'bf60fb3a-3b37-4256-b7d6-6491bf800f0d', '7de42cab-f048-47bd-89b0-ab5604cab39f', 'transferred_to', 3.62, '{}'::jsonb,
                 NOW() - interval '128 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('be4ae6af-8f78-401a-a7e3-0ef798a25417', '49059f98-f464-499a-9f9e-5604108027ae', '2b3e4659-7a01-44c1-8dae-8c280ae9ac57', 'uses_number', 16.53, '{}'::jsonb,
                 NOW() - interval '23 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('198df0f3-be0b-4818-8cd8-dfb2b91bb64a', '19ee01c5-2fcc-4d8a-9b1c-d71b0ddea7db', '49059f98-f464-499a-9f9e-5604108027ae', 'reported_by', 24.20, '{}'::jsonb,
                 NOW() - interval '170 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('361481aa-5021-4e11-a32e-f902a23e5819', '16503e2a-1a03-48ab-a0a4-21cd5dc9a677', 'd1d04507-4d3c-4b4f-93d3-b9e0ea716ebd', 'transferred_to', 7.21, '{}'::jsonb,
                 NOW() - interval '262 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('73ff8025-21dc-44da-8200-269315b3dc58', '1fd47cfe-f8c3-4ea2-980e-bf7514ac5e9c', '7de42cab-f048-47bd-89b0-ab5604cab39f', 'owns_account', 11.70, '{}'::jsonb,
                 NOW() - interval '201 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('1b14d10a-0130-4de4-9a39-c358168a295b', '0adcebcc-d7dc-42d5-8851-1353964f611e', '49059f98-f464-499a-9f9e-5604108027ae', 'uses_number', 9.28, '{}'::jsonb,
                 NOW() - interval '13 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('3a0dcccb-12c0-40ce-a4b5-8254143cfb84', '16503e2a-1a03-48ab-a0a4-21cd5dc9a677', '82d1a388-a107-4386-81e7-4e80f8bb0067', 'reported_by', 23.09, '{}'::jsonb,
                 NOW() - interval '44 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('d7073986-4744-4bee-a7e8-b70b9d3268ec', 'c8a2fc3a-14e5-4916-a455-05cb605dc540', 'bf34659a-0644-4929-8d17-452df2a70dfd', 'uses_number', 9.36, '{}'::jsonb,
                 NOW() - interval '176 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('1065e02b-8ed1-49c1-baaf-8d67c3436eea', 'bf60fb3a-3b37-4256-b7d6-6491bf800f0d', '129adb44-c0b2-44eb-860e-2e6f616384b9', 'linked_to', 9.36, '{}'::jsonb,
                 NOW() - interval '50 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('b88e4c80-f73d-45e4-88d5-b96beb2d18c7', 'bf34659a-0644-4929-8d17-452df2a70dfd', '0a6457b4-a7a1-482e-9a8e-a599c986469b', 'linked_to', 8.65, '{}'::jsonb,
                 NOW() - interval '154 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('5522a80a-2ffc-4a5e-8996-51914bb72d43', 'bf60fb3a-3b37-4256-b7d6-6491bf800f0d', '0a6457b4-a7a1-482e-9a8e-a599c986469b', 'transferred_to', 1.54, '{}'::jsonb,
                 NOW() - interval '176 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ab6d4fad-a2e6-4213-b06f-3d0981776924', '16503e2a-1a03-48ab-a0a4-21cd5dc9a677', '49059f98-f464-499a-9f9e-5604108027ae', 'uses_number', 23.32, '{}'::jsonb,
                 NOW() - interval '125 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('c7af2888-a365-4ad4-ad43-a1bfec0b0ba3', '8a6e742d-1818-4d9e-8013-bcd4177200a7', '7de42cab-f048-47bd-89b0-ab5604cab39f', 'uses_number', 8.94, '{}'::jsonb,
                 NOW() - interval '219 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('2db7f386-8a51-4014-92b4-7e296dd2d2cd', '4e0488be-17a0-4774-b5f4-ac7f57ae9470', 'bf60fb3a-3b37-4256-b7d6-6491bf800f0d', 'reported_by', 16.11, '{}'::jsonb,
                 NOW() - interval '96 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('e67a70b0-7b39-4c89-b5c0-ffe513507bb9', '49059f98-f464-499a-9f9e-5604108027ae', '09ba0704-e084-4e2e-9490-0ecc9def9b7b', 'reported_by', 1.70, '{}'::jsonb,
                 NOW() - interval '102 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('bc4171dd-b34c-407b-9c8f-5f71b3710b82', '9a3bcf18-ee8c-4dc0-8ad4-3408785b4c22', '09ba0704-e084-4e2e-9490-0ecc9def9b7b', 'reported_by', 1.11, '{}'::jsonb,
                 NOW() - interval '110 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('d7e7e66f-f6af-4a16-8c65-4648a5d307d5', 'df4b5f72-f2b3-40e4-9337-bb1f86058aea', '0adcebcc-d7dc-42d5-8851-1353964f611e', 'transferred_to', 14.86, '{}'::jsonb,
                 NOW() - interval '275 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('90a48c95-2485-467b-8fdf-a5550ccbcb36', '2b3e4659-7a01-44c1-8dae-8c280ae9ac57', 'e513f62b-ba06-404f-b02f-cf3b67e6283a', 'owns_account', 11.98, '{}'::jsonb,
                 NOW() - interval '135 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('c4354873-de6d-44ee-a02c-28c82bdaf679', '425e3c57-320a-4d83-a0cc-208064db5786', 'b9eeda0a-bb63-49e1-821b-22c0a12a013c', 'connected_from', 15.33, '{}'::jsonb,
                 NOW() - interval '201 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('e560220a-d375-4ada-9033-378960da789b', 'f4e54e0c-e323-4cd7-9a4e-fc0dd3b9026d', '3aa86899-41f4-48bc-9aba-dacf52c5d1e8', 'linked_to', 15.82, '{}'::jsonb,
                 NOW() - interval '153 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('20916d0f-567e-4dc9-89e4-4cbda0debf3a', 'b1cdc6d4-5382-4628-a137-7250fc5b482c', 'b5338512-5745-4680-be80-d3f9ac9322a0', 'uses_number', 8.52, '{}'::jsonb,
                 NOW() - interval '123 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('1b45fc94-7565-46fa-bd3b-7f47f3fab8bc', '7e45636b-10dd-41cf-9664-aea86712fe21', 'e50db8f6-0a23-4c78-9a2a-bf0951a259db', 'connected_from', 17.64, '{}'::jsonb,
                 NOW() - interval '262 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('e68f3ada-f636-4da5-a298-fe3ed7b65290', '4f7e2c5b-93f5-48f7-bcbc-69df0d427433', '0b328c4b-fecb-40f9-b76d-5b2abd33546b', 'uses_number', 14.80, '{}'::jsonb,
                 NOW() - interval '217 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('2c2eb50f-e8e4-420c-9b2f-bb0b3ea325cf', '7d2bdda8-38e8-4339-a7d0-a3ef694f519e', '9b4c109d-36ae-43b3-a553-1667ea131ae5', 'uses_number', 14.32, '{}'::jsonb,
                 NOW() - interval '251 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('22a917b5-b06c-4683-98af-518606f6f4d2', '9e7f82dc-3a0f-40f1-b34a-bd7b3d0147e6', 'e50db8f6-0a23-4c78-9a2a-bf0951a259db', 'connected_from', 21.21, '{}'::jsonb,
                 NOW() - interval '28 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('08558060-6753-4b29-803d-cf26fe170e0a', 'e9067e16-7368-459d-ac9f-bc21dff20791', '7d2bdda8-38e8-4339-a7d0-a3ef694f519e', 'uses_number', 5.68, '{}'::jsonb,
                 NOW() - interval '197 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ea100443-9698-4d63-b7b5-19247963ea28', '7fd97fca-c7d9-4fd4-ad6d-699f4f0cddbc', '9b4c109d-36ae-43b3-a553-1667ea131ae5', 'linked_to', 10.82, '{}'::jsonb,
                 NOW() - interval '252 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('71e478ab-e735-4044-9f83-f00ca0e88236', '9b5118de-22be-43b2-ac26-5849b30678c0', 'f7d45c99-7fe5-4c94-b453-7854c78d65ac', 'linked_to', 12.73, '{}'::jsonb,
                 NOW() - interval '43 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('aec65224-d2ab-453c-9deb-03806ce872e6', 'e9067e16-7368-459d-ac9f-bc21dff20791', '1cfbccbd-a228-484b-a6ac-6f17b3655100', 'owns_account', 8.01, '{}'::jsonb,
                 NOW() - interval '141 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('e9e9807f-2617-4a74-819c-6f58d5980564', '54d62db7-2af4-444f-a83f-f664124ca252', '9ec64938-e4b0-49fa-9c47-e4d14701fc59', 'uses_number', 19.74, '{}'::jsonb,
                 NOW() - interval '290 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('38a0485e-666a-4003-9d4d-2f1d748e3fe7', '900d7239-8f6b-4c18-9ae4-c8cb6fda1c0b', '7d2bdda8-38e8-4339-a7d0-a3ef694f519e', 'transferred_to', 14.75, '{}'::jsonb,
                 NOW() - interval '138 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('a82b62b9-3ffb-4c93-8ca6-7f86b471d36f', 'f7d45c99-7fe5-4c94-b453-7854c78d65ac', 'f4e54e0c-e323-4cd7-9a4e-fc0dd3b9026d', 'called', 19.24, '{}'::jsonb,
                 NOW() - interval '226 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('625b6355-633a-4474-a63d-b19a6a05a001', '0ac06981-2709-4295-a746-a7904938d7fe', '4f7e2c5b-93f5-48f7-bcbc-69df0d427433', 'transferred_to', 18.66, '{}'::jsonb,
                 NOW() - interval '127 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('f86a5858-672d-4844-8127-a5c5a2b971e5', '3aa86899-41f4-48bc-9aba-dacf52c5d1e8', '1a58ccc8-0ac1-4bc4-8f84-ff79ff4073f3', 'linked_to', 7.31, '{}'::jsonb,
                 NOW() - interval '45 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('0dda4f7d-bffb-4a6f-9302-5c1658aeef6e', '3aa86899-41f4-48bc-9aba-dacf52c5d1e8', '7e45636b-10dd-41cf-9664-aea86712fe21', 'owns_account', 6.04, '{}'::jsonb,
                 NOW() - interval '180 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('31335569-51ef-4301-9417-41b9f84a4226', '0b328c4b-fecb-40f9-b76d-5b2abd33546b', '9b4c109d-36ae-43b3-a553-1667ea131ae5', 'reported_by', 4.98, '{}'::jsonb,
                 NOW() - interval '72 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('0548c38f-38e3-4d51-a90d-f8fdefa91fc1', 'f7d45c99-7fe5-4c94-b453-7854c78d65ac', '0ac06981-2709-4295-a746-a7904938d7fe', 'called', 14.68, '{}'::jsonb,
                 NOW() - interval '273 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('90057873-7324-41d8-acda-449b58370b96', '0b328c4b-fecb-40f9-b76d-5b2abd33546b', '54d62db7-2af4-444f-a83f-f664124ca252', 'uses_number', 8.77, '{}'::jsonb,
                 NOW() - interval '150 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('8e202d1e-a6e6-4a33-8ebe-c98e03b8c585', 'b1cdc6d4-5382-4628-a137-7250fc5b482c', 'f8592779-aaef-4965-85e7-6cadce0115ba', 'transferred_to', 4.25, '{}'::jsonb,
                 NOW() - interval '211 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('14868624-2d53-475c-ba62-41c7a4fb88b5', 'f8592779-aaef-4965-85e7-6cadce0115ba', '3aa86899-41f4-48bc-9aba-dacf52c5d1e8', 'uses_number', 17.83, '{}'::jsonb,
                 NOW() - interval '68 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('26b3aa0b-2709-4ff8-b527-1ba8c95763e0', '9e7f82dc-3a0f-40f1-b34a-bd7b3d0147e6', '9b5118de-22be-43b2-ac26-5849b30678c0', 'connected_from', 20.88, '{}'::jsonb,
                 NOW() - interval '202 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('e9f73a96-30b7-4225-96ae-47ced77cb891', '9e7f82dc-3a0f-40f1-b34a-bd7b3d0147e6', 'b1cdc6d4-5382-4628-a137-7250fc5b482c', 'uses_device', 16.07, '{}'::jsonb,
                 NOW() - interval '193 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('b1e0744b-42bf-4a0e-9d14-7406f8fb88e7', 'b5338512-5745-4680-be80-d3f9ac9322a0', '9b4c109d-36ae-43b3-a553-1667ea131ae5', 'transferred_to', 10.67, '{}'::jsonb,
                 NOW() - interval '143 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('57aef3a1-463c-451e-ac9a-28f096e60fd0', 'f4e54e0c-e323-4cd7-9a4e-fc0dd3b9026d', 'd32d4ae7-05af-4479-afaa-a51b1189842d', 'linked_to', 8.85, '{}'::jsonb,
                 NOW() - interval '2 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ea7bd759-3540-424e-aee3-3206f40c5ce0', 'b5338512-5745-4680-be80-d3f9ac9322a0', '1758a1da-5c6e-4fba-a0ce-77f7216f3167', 'linked_to', 16.24, '{}'::jsonb,
                 NOW() - interval '184 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('518bc985-aeba-4150-a6e9-c9adb29fe637', '1cfbccbd-a228-484b-a6ac-6f17b3655100', '54d62db7-2af4-444f-a83f-f664124ca252', 'reported_by', 6.23, '{}'::jsonb,
                 NOW() - interval '220 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('7c351b71-ee8a-4235-b9e4-047cf471158d', '7d2bdda8-38e8-4339-a7d0-a3ef694f519e', 'f8592779-aaef-4965-85e7-6cadce0115ba', 'connected_from', 20.88, '{}'::jsonb,
                 NOW() - interval '173 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('8037db5f-49c4-4b30-8c16-c80003307415', 'b1cdc6d4-5382-4628-a137-7250fc5b482c', '9e7f82dc-3a0f-40f1-b34a-bd7b3d0147e6', 'linked_to', 19.92, '{}'::jsonb,
                 NOW() - interval '25 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('c6f17d09-d187-46f1-9402-648ef47f82f6', '7e45636b-10dd-41cf-9664-aea86712fe21', '9b4c109d-36ae-43b3-a553-1667ea131ae5', 'linked_to', 1.39, '{}'::jsonb,
                 NOW() - interval '81 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('68a19348-b862-453b-b03d-551d1ef175b7', 'd32d4ae7-05af-4479-afaa-a51b1189842d', 'e9067e16-7368-459d-ac9f-bc21dff20791', 'reported_by', 5.86, '{}'::jsonb,
                 NOW() - interval '68 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('8385ca3b-ca7e-4d24-b6f0-9015bc4537c9', '9ec64938-e4b0-49fa-9c47-e4d14701fc59', 'e50db8f6-0a23-4c78-9a2a-bf0951a259db', 'uses_device', 3.24, '{}'::jsonb,
                 NOW() - interval '185 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('15e2c316-d952-4523-9973-ce3da87e557f', 'b5338512-5745-4680-be80-d3f9ac9322a0', 'f4e54e0c-e323-4cd7-9a4e-fc0dd3b9026d', 'uses_number', 2.24, '{}'::jsonb,
                 NOW() - interval '157 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('a8af9b17-4169-4f5b-84f3-e153fb72d2b9', '9b5118de-22be-43b2-ac26-5849b30678c0', '900d7239-8f6b-4c18-9ae4-c8cb6fda1c0b', 'owns_account', 11.30, '{}'::jsonb,
                 NOW() - interval '47 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('a6de0085-38e1-474a-a070-48a1de45cbca', '7e45636b-10dd-41cf-9664-aea86712fe21', 'e9067e16-7368-459d-ac9f-bc21dff20791', 'owns_account', 12.44, '{}'::jsonb,
                 NOW() - interval '68 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('2adedcc3-b102-4fb6-bd78-4db048b648ac', '5108d8cd-1406-4580-b094-9f8d02e0ccdb', '7fd97fca-c7d9-4fd4-ad6d-699f4f0cddbc', 'linked_to', 1.22, '{}'::jsonb,
                 NOW() - interval '176 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('a7d82835-ba03-4308-ad49-c481912db2e4', '3aa86899-41f4-48bc-9aba-dacf52c5d1e8', '4f7e2c5b-93f5-48f7-bcbc-69df0d427433', 'uses_number', 12.46, '{}'::jsonb,
                 NOW() - interval '118 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('68f6e767-a3d6-45fd-9496-e0c997e095f0', 'b5338512-5745-4680-be80-d3f9ac9322a0', '1758a1da-5c6e-4fba-a0ce-77f7216f3167', 'transferred_to', 3.48, '{}'::jsonb,
                 NOW() - interval '189 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('12bea48a-b3a6-4a71-b6f9-1756fc8371ed', '9e7f82dc-3a0f-40f1-b34a-bd7b3d0147e6', '437ee980-5602-4683-8d3c-93959d21e09c', 'uses_number', 16.40, '{}'::jsonb,
                 NOW() - interval '74 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('893e789b-580c-4498-9641-3f755029c85c', '7fd97fca-c7d9-4fd4-ad6d-699f4f0cddbc', 'b1cdc6d4-5382-4628-a137-7250fc5b482c', 'called', 15.65, '{}'::jsonb,
                 NOW() - interval '85 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ab5005eb-d1fa-44d7-96e1-7a79aea490d2', 'f4e54e0c-e323-4cd7-9a4e-fc0dd3b9026d', '1758a1da-5c6e-4fba-a0ce-77f7216f3167', 'owns_account', 16.07, '{}'::jsonb,
                 NOW() - interval '78 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('fac8036b-8ae6-48c3-acec-9019ea01f691', '0b328c4b-fecb-40f9-b76d-5b2abd33546b', '28057f03-f016-44d3-8f3a-33db25f272cc', 'linked_to', 21.64, '{}'::jsonb,
                 NOW() - interval '45 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('bfa5854e-5348-4256-b2d1-bffa59124773', '9e7f82dc-3a0f-40f1-b34a-bd7b3d0147e6', '900d7239-8f6b-4c18-9ae4-c8cb6fda1c0b', 'transferred_to', 15.15, '{}'::jsonb,
                 NOW() - interval '197 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('8119c89b-2efc-4860-859e-a6219429e454', '4f7e2c5b-93f5-48f7-bcbc-69df0d427433', 'e47f1f26-cfc6-49d0-aac1-dbc9b8a8e528', 'uses_number', 6.95, '{}'::jsonb,
                 NOW() - interval '44 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('cd009786-886f-4575-9d2f-97f623e5a28e', '54d62db7-2af4-444f-a83f-f664124ca252', '0b328c4b-fecb-40f9-b76d-5b2abd33546b', 'uses_device', 19.70, '{}'::jsonb,
                 NOW() - interval '14 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('a0d1bcd0-4935-4992-ae26-01c418983f94', '9ec64938-e4b0-49fa-9c47-e4d14701fc59', '0ac06981-2709-4295-a746-a7904938d7fe', 'owns_account', 18.95, '{}'::jsonb,
                 NOW() - interval '152 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('1940c2ff-40ad-4ed4-93aa-ab24d87b564a', '1a58ccc8-0ac1-4bc4-8f84-ff79ff4073f3', '1cfbccbd-a228-484b-a6ac-6f17b3655100', 'owns_account', 12.88, '{}'::jsonb,
                 NOW() - interval '58 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('56773202-13f9-4676-a941-0f17e2640ba4', '7d2bdda8-38e8-4339-a7d0-a3ef694f519e', '9b4c109d-36ae-43b3-a553-1667ea131ae5', 'transferred_to', 13.68, '{}'::jsonb,
                 NOW() - interval '7 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('83bb34e8-ea88-47b7-bffd-2f98c8684962', 'e47f1f26-cfc6-49d0-aac1-dbc9b8a8e528', '9e7f82dc-3a0f-40f1-b34a-bd7b3d0147e6', 'reported_by', 21.66, '{}'::jsonb,
                 NOW() - interval '292 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('3c25a6de-839e-4b68-8543-6585cb070a3b', 'f4e54e0c-e323-4cd7-9a4e-fc0dd3b9026d', '54d62db7-2af4-444f-a83f-f664124ca252', 'uses_number', 19.31, '{}'::jsonb,
                 NOW() - interval '38 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('474ffe86-bc90-477b-8724-a1c6e981e245', 'b1cdc6d4-5382-4628-a137-7250fc5b482c', 'b5338512-5745-4680-be80-d3f9ac9322a0', 'called', 7.29, '{}'::jsonb,
                 NOW() - interval '21 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('13daf668-7739-4884-a6a5-aff34dc8eaee', 'a76f1d08-5697-4bea-830d-0b2960bc22e9', 'ac642857-6013-45c4-8ea6-c7ae64b4b271', 'reported_by', 11.17, '{}'::jsonb,
                 NOW() - interval '206 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('2a04fa68-ca63-473c-96ea-05f219c35a99', '1fdfe259-8382-4714-bd12-e4a9c9d32007', 'be96fae5-420e-4a90-8018-d048622bbbe5', 'uses_number', 7.66, '{}'::jsonb,
                 NOW() - interval '159 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('77d7b6de-6dd8-421c-922b-828ed3a5e2e1', 'a76f1d08-5697-4bea-830d-0b2960bc22e9', 'c6ee2223-b96c-40af-b17b-23c1786a40cf', 'uses_number', 13.87, '{}'::jsonb,
                 NOW() - interval '201 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('239657c9-e3d4-4269-b169-35b85e78d65d', '1fdfe259-8382-4714-bd12-e4a9c9d32007', 'c61620b7-834b-4831-bfe2-189fd64e710a', 'transferred_to', 8.44, '{}'::jsonb,
                 NOW() - interval '224 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('b8bf81f1-3324-4cab-9360-b403d534b4f1', '238e4285-9571-4b3b-a192-fbc4a715790a', '25a3479f-0597-46f4-89c5-666108cfba65', 'owns_account', 3.07, '{}'::jsonb,
                 NOW() - interval '223 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('683de569-1852-4dcc-a97d-dfa5a565758b', '6a5d2fe7-78e6-4001-b3e2-0ca03b7332b6', 'c8bedcce-c8db-4e15-a9f1-cc3355093ee6', 'called', 8.42, '{}'::jsonb,
                 NOW() - interval '90 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('b6393b56-40d4-4f51-8320-6a352e4e8bd4', '1b0d5630-551e-48c9-b0e1-a0a8958d5bba', 'a7567274-9370-41c0-9af1-765e783e9c48', 'uses_number', 17.84, '{}'::jsonb,
                 NOW() - interval '84 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('e48a72af-d9d5-445d-8f7d-0e0fc73c8bc2', '7de08716-7100-4055-98b8-1b706b7bafb0', 'a76f1d08-5697-4bea-830d-0b2960bc22e9', 'uses_device', 5.01, '{}'::jsonb,
                 NOW() - interval '65 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('4f9e7c0c-59bf-4c6a-86b9-cc8fbeef5774', '8b086099-5521-466a-902a-3c87e839cdd8', 'd784ba7e-9706-43a4-935b-9b953787be18', 'transferred_to', 19.51, '{}'::jsonb,
                 NOW() - interval '16 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('0cb23af5-ffbd-4268-a3d7-7fba66f069ff', 'ed5b9337-a5d8-40ae-a4f3-6faf89159c53', '8b086099-5521-466a-902a-3c87e839cdd8', 'transferred_to', 7.31, '{}'::jsonb,
                 NOW() - interval '296 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('b92332a0-ea7f-4644-b077-8c2457584e7a', '4ac22938-0413-4fea-aa04-1c47fb6b6a1c', '79ddffc9-9c15-444b-bf2d-3e0b5dad02f4', 'linked_to', 13.26, '{}'::jsonb,
                 NOW() - interval '29 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('10100dc9-4179-40bb-86e8-da0ca714cf3d', 'f5c51b83-3838-48fe-b1f8-919459681d42', 'f78481ca-a8ae-449c-871c-157473b44be7', 'connected_from', 4.78, '{}'::jsonb,
                 NOW() - interval '53 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('fcac2a53-7d2d-4b9d-b92d-f697719d774b', 'c61620b7-834b-4831-bfe2-189fd64e710a', 'd784ba7e-9706-43a4-935b-9b953787be18', 'transferred_to', 6.48, '{}'::jsonb,
                 NOW() - interval '261 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('9dc52fcc-f22f-4453-a227-5400e80728a0', '25a3479f-0597-46f4-89c5-666108cfba65', '1b0d5630-551e-48c9-b0e1-a0a8958d5bba', 'owns_account', 2.10, '{}'::jsonb,
                 NOW() - interval '187 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('3274c8a3-08e4-444b-933f-3b7ea2e75af0', 'bc8f19ac-6d56-444d-9c70-a050fe0cbaa9', 'f78481ca-a8ae-449c-871c-157473b44be7', 'called', 14.27, '{}'::jsonb,
                 NOW() - interval '215 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('87718423-f16e-484a-b8d2-c2a8df6f63e9', '461393fa-eff7-4a51-b018-619964e962e7', '238e4285-9571-4b3b-a192-fbc4a715790a', 'reported_by', 22.98, '{}'::jsonb,
                 NOW() - interval '164 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ba30c04d-cd84-4f4e-b65d-de0179c74cfc', '4ac22938-0413-4fea-aa04-1c47fb6b6a1c', 'f5c51b83-3838-48fe-b1f8-919459681d42', 'connected_from', 3.87, '{}'::jsonb,
                 NOW() - interval '27 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('cd5a0721-c56d-46bd-b910-72537dba65d1', '238e4285-9571-4b3b-a192-fbc4a715790a', 'a76f1d08-5697-4bea-830d-0b2960bc22e9', 'called', 23.90, '{}'::jsonb,
                 NOW() - interval '36 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('2abf3cee-b488-4780-bd98-467a9c62b56b', 'ac642857-6013-45c4-8ea6-c7ae64b4b271', '461393fa-eff7-4a51-b018-619964e962e7', 'transferred_to', 14.27, '{}'::jsonb,
                 NOW() - interval '5 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('b7314a34-8e7a-42bc-82d6-93928d3d4976', 'c6ee2223-b96c-40af-b17b-23c1786a40cf', 'ac642857-6013-45c4-8ea6-c7ae64b4b271', 'uses_device', 18.75, '{}'::jsonb,
                 NOW() - interval '125 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('e30a6b24-1492-4b17-8f2f-bd9e143a1f57', '7de08716-7100-4055-98b8-1b706b7bafb0', 'f5c51b83-3838-48fe-b1f8-919459681d42', 'linked_to', 24.95, '{}'::jsonb,
                 NOW() - interval '101 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ab9232b3-2639-473a-b77a-09978b4a2631', 'be96fae5-420e-4a90-8018-d048622bbbe5', '238e4285-9571-4b3b-a192-fbc4a715790a', 'uses_number', 1.15, '{}'::jsonb,
                 NOW() - interval '210 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('3a905934-a8a7-4859-a0f1-0a10386a93a5', '238e4285-9571-4b3b-a192-fbc4a715790a', 'be96fae5-420e-4a90-8018-d048622bbbe5', 'connected_from', 16.26, '{}'::jsonb,
                 NOW() - interval '5 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('66ef0435-03d2-4079-9dd9-712fa60fb17c', '1b0d5630-551e-48c9-b0e1-a0a8958d5bba', 'c61620b7-834b-4831-bfe2-189fd64e710a', 'reported_by', 21.38, '{}'::jsonb,
                 NOW() - interval '158 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('c94d130b-d5be-4118-8fcd-513d339a2381', 'c6ee2223-b96c-40af-b17b-23c1786a40cf', 'a76f1d08-5697-4bea-830d-0b2960bc22e9', 'owns_account', 11.08, '{}'::jsonb,
                 NOW() - interval '31 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('05376627-59ea-4d9c-a2a6-4d21b14f399e', 'a7567274-9370-41c0-9af1-765e783e9c48', '8b086099-5521-466a-902a-3c87e839cdd8', 'transferred_to', 2.05, '{}'::jsonb,
                 NOW() - interval '119 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('5d61704e-31ba-4392-909a-f5fbee0b9f4a', 'ed5b9337-a5d8-40ae-a4f3-6faf89159c53', 'a7567274-9370-41c0-9af1-765e783e9c48', 'connected_from', 12.00, '{}'::jsonb,
                 NOW() - interval '44 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('fc172fb5-62f8-4a38-9605-fede7f9eb047', '5f772a17-f7f5-45cd-a1d7-d85d994ea666', 'a76f1d08-5697-4bea-830d-0b2960bc22e9', 'uses_number', 16.29, '{}'::jsonb,
                 NOW() - interval '202 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('43d68208-ec29-43d7-947c-f459100fb2c6', 'f5c51b83-3838-48fe-b1f8-919459681d42', '25a3479f-0597-46f4-89c5-666108cfba65', 'reported_by', 16.90, '{}'::jsonb,
                 NOW() - interval '67 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('290ffebd-8905-4ac0-91b7-709c325d5085', 'ac642857-6013-45c4-8ea6-c7ae64b4b271', '8b086099-5521-466a-902a-3c87e839cdd8', 'connected_from', 23.23, '{}'::jsonb,
                 NOW() - interval '202 days', NOW() - interval '5 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('3cf3658e-fd24-4067-9c62-a38521fd1b7c', 'd784ba7e-9706-43a4-935b-9b953787be18', '461393fa-eff7-4a51-b018-619964e962e7', 'connected_from', 11.87, '{}'::jsonb,
                 NOW() - interval '120 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('05008cb9-43a6-4bb7-9745-56c54563daa4', 'c6ee2223-b96c-40af-b17b-23c1786a40cf', 'bc8f19ac-6d56-444d-9c70-a050fe0cbaa9', 'transferred_to', 4.73, '{}'::jsonb,
                 NOW() - interval '85 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('d1343cfe-62ef-403f-958c-e5a570c0f5b3', '6a5d2fe7-78e6-4001-b3e2-0ca03b7332b6', '461393fa-eff7-4a51-b018-619964e962e7', 'reported_by', 3.90, '{}'::jsonb,
                 NOW() - interval '184 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('7c66f75b-efc6-4b3a-9a20-6d8f947b3d53', '6a5d2fe7-78e6-4001-b3e2-0ca03b7332b6', 'ac642857-6013-45c4-8ea6-c7ae64b4b271', 'linked_to', 7.36, '{}'::jsonb,
                 NOW() - interval '62 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('48c39b40-a0cb-434e-bfc9-e4ce53f5a4d8', 'f78481ca-a8ae-449c-871c-157473b44be7', 'c61620b7-834b-4831-bfe2-189fd64e710a', 'uses_device', 20.83, '{}'::jsonb,
                 NOW() - interval '21 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('c392f491-02bd-4f0c-9ff9-d6510ccf0cde', '461393fa-eff7-4a51-b018-619964e962e7', 'bc8f19ac-6d56-444d-9c70-a050fe0cbaa9', 'transferred_to', 18.07, '{}'::jsonb,
                 NOW() - interval '183 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('078998e5-e586-4af8-bb1c-42f378102247', 'a76f1d08-5697-4bea-830d-0b2960bc22e9', '25a3479f-0597-46f4-89c5-666108cfba65', 'uses_device', 7.24, '{}'::jsonb,
                 NOW() - interval '90 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('07cf1dbe-a96a-47ac-af7c-3894546a4f2d', 'cbaee268-8fac-4cc0-9b6e-54ae42d025a4', '6a5d2fe7-78e6-4001-b3e2-0ca03b7332b6', 'owns_account', 3.27, '{}'::jsonb,
                 NOW() - interval '53 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('bb86116c-964a-451c-9116-65a147d6f8b1', '5f772a17-f7f5-45cd-a1d7-d85d994ea666', '1b0d5630-551e-48c9-b0e1-a0a8958d5bba', 'called', 20.93, '{}'::jsonb,
                 NOW() - interval '114 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('bd5a7267-5034-4ad1-b328-aa5d978699e7', 'c6ee2223-b96c-40af-b17b-23c1786a40cf', 'cbaee268-8fac-4cc0-9b6e-54ae42d025a4', 'connected_from', 17.47, '{}'::jsonb,
                 NOW() - interval '44 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('5085fb5e-c298-4d62-9bc3-94fd74d4c87f', 'f5c51b83-3838-48fe-b1f8-919459681d42', '8b086099-5521-466a-902a-3c87e839cdd8', 'transferred_to', 1.52, '{}'::jsonb,
                 NOW() - interval '34 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('fb18ff7f-1710-48b3-900d-46dff2dddb48', '1fdfe259-8382-4714-bd12-e4a9c9d32007', '6a5d2fe7-78e6-4001-b3e2-0ca03b7332b6', 'uses_number', 3.21, '{}'::jsonb,
                 NOW() - interval '170 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ed58f687-2177-45f9-a44b-7f120eba98d8', '25a3479f-0597-46f4-89c5-666108cfba65', '6a5d2fe7-78e6-4001-b3e2-0ca03b7332b6', 'called', 5.03, '{}'::jsonb,
                 NOW() - interval '294 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('a502e4a7-3fc4-4a81-a746-1d6bf477097a', 'd784ba7e-9706-43a4-935b-9b953787be18', 'cbaee268-8fac-4cc0-9b6e-54ae42d025a4', 'linked_to', 1.71, '{}'::jsonb,
                 NOW() - interval '219 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('508278d6-89a6-4840-a24e-411174784a9a', '7de08716-7100-4055-98b8-1b706b7bafb0', 'c6ee2223-b96c-40af-b17b-23c1786a40cf', 'uses_number', 7.60, '{}'::jsonb,
                 NOW() - interval '229 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('8922f8e6-ecbd-4bfb-9cf7-d56fcf679e97', '25a3479f-0597-46f4-89c5-666108cfba65', 'c8bedcce-c8db-4e15-a9f1-cc3355093ee6', 'owns_account', 16.53, '{}'::jsonb,
                 NOW() - interval '256 days', NOW() - interval '3 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('0f639ade-7f5a-40e4-84a2-6c3ed710e3a2', 'be96fae5-420e-4a90-8018-d048622bbbe5', '79ddffc9-9c15-444b-bf2d-3e0b5dad02f4', 'called', 3.11, '{}'::jsonb,
                 NOW() - interval '197 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('269f9f99-8212-4456-81fe-6ab0d24f985b', 'ed5b9337-a5d8-40ae-a4f3-6faf89159c53', 'c6ee2223-b96c-40af-b17b-23c1786a40cf', 'owns_account', 16.14, '{}'::jsonb,
                 NOW() - interval '279 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('ee8903ad-374a-4f57-ae74-e6598de6e859', 'cbaee268-8fac-4cc0-9b6e-54ae42d025a4', 'a7567274-9370-41c0-9af1-765e783e9c48', 'connected_from', 12.51, '{}'::jsonb,
                 NOW() - interval '249 days', NOW() - interval '2 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('0a6b9c40-b630-45c2-8fc0-34b994b60791', 'f5c51b83-3838-48fe-b1f8-919459681d42', 'a76f1d08-5697-4bea-830d-0b2960bc22e9', 'connected_from', 10.32, '{}'::jsonb,
                 NOW() - interval '93 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('31663b2d-150b-47f6-b085-a736b4023ddc', '461393fa-eff7-4a51-b018-619964e962e7', 'c8bedcce-c8db-4e15-a9f1-cc3355093ee6', 'owns_account', 1.70, '{}'::jsonb,
                 NOW() - interval '144 days', NOW() - interval '0 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('f437af41-dce4-4896-aeb3-b3d0c2670068', '79ddffc9-9c15-444b-bf2d-3e0b5dad02f4', 'a76f1d08-5697-4bea-830d-0b2960bc22e9', 'connected_from', 19.40, '{}'::jsonb,
                 NOW() - interval '120 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('9873ef3f-cb7c-44b4-bde1-5ab05f72ddc7', '5f772a17-f7f5-45cd-a1d7-d85d994ea666', '238e4285-9571-4b3b-a192-fbc4a715790a', 'owns_account', 7.40, '{}'::jsonb,
                 NOW() - interval '29 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('97d9f320-de2f-4c14-a149-b0022cb714f9', 'f5c51b83-3838-48fe-b1f8-919459681d42', 'cbaee268-8fac-4cc0-9b6e-54ae42d025a4', 'connected_from', 23.44, '{}'::jsonb,
                 NOW() - interval '89 days', NOW() - interval '1 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('4370c99e-0231-43a4-8fd7-a856e4a72b65', '238e4285-9571-4b3b-a192-fbc4a715790a', 'f5c51b83-3838-48fe-b1f8-919459681d42', 'connected_from', 20.35, '{}'::jsonb,
                 NOW() - interval '184 days', NOW() - interval '4 days');
INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('af40b242-71ed-466e-b904-af3cd2f657e5', '1b0d5630-551e-48c9-b0e1-a0a8958d5bba', 'a7567274-9370-41c0-9af1-765e783e9c48', 'connected_from', 23.74, '{}'::jsonb,
                 NOW() - interval '289 days', NOW() - interval '1 days');
-- total edges generated: 213

-- geo_intel.incidents
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b917517c-6d75-462b-b86b-98c2387556b6', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.697601, 12.897058), 4326),
             'Karnataka', 'Bangalore', '446021',
             'medium', 738202.45,
             'scam_sentinel',
             NOW() - interval '29 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'dd49175d-aee9-4a45-99ae-fde34cfd6cf7', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.880554, 18.983147), 4326),
             'Maharashtra', 'Mumbai', '560991',
             'medium', 306189.25,
             'fraud_graph',
             NOW() - interval '175 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '54a94528-6e31-4426-b2d8-7c8ae1894d1d', 'ficn_seizure',
             'Ficn Seizure reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.668857, 13.079695), 4326),
             'Karnataka', 'Bangalore', '438721',
             'low', 881980.72,
             'fraud_graph',
             NOW() - interval '57 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '020e0164-2cdb-4630-89f0-99eb3cbf4cd2', 'ficn_seizure',
             'Ficn Seizure reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.542112, 17.472134), 4326),
             'Telangana', 'Hyderabad', '573575',
             'high', 596415.37,
             'scam_sentinel',
             NOW() - interval '173 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'c26731ac-7eb9-498d-89e1-6a4409aded20', 'investment_scam',
             'Investment Scam reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.013002, 28.538206), 4326),
             'Delhi', 'Delhi', '527716',
             'high', 975524.50,
             'fraud_graph',
             NOW() - interval '363 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7b67556e-bdbe-4787-a238-50b0e3911a02', 'ficn_seizure',
             'Ficn Seizure reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.535769, 17.438712), 4326),
             'Telangana', 'Hyderabad', '554389',
             'medium', 1222609.08,
             'note_verify',
             NOW() - interval '158 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'ac03230f-1e24-4945-b7b8-93b79f0b8f3d', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.535542, 12.923629), 4326),
             'Karnataka', 'Bangalore', '550165',
             'critical', 590444.13,
             'scam_sentinel',
             NOW() - interval '94 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'c87abb00-0c2b-4b36-bf37-d931e1077b88', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.693506, 13.08026), 4326),
             'Karnataka', 'Bangalore', '427291',
             'high', 1405348.25,
             'fraud_graph',
             NOW() - interval '170 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '6ff3188b-ef14-4af1-b72f-0aeae3f0e9b2', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.696476, 12.909499), 4326),
             'Karnataka', 'Bangalore', '423258',
             'high', 1233384.40,
             'citizen_shield',
             NOW() - interval '229 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '2bc97a06-cfb4-46a3-93b5-5c4e502bd6b8', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.915567, 18.97968), 4326),
             'Maharashtra', 'Mumbai', '428320',
             'medium', 1082018.31,
             'scam_sentinel',
             NOW() - interval '198 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'f229ae00-b963-4c44-ae39-fb89cb5ad39e', 'investment_scam',
             'Investment Scam reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.016535, 28.617503), 4326),
             'Delhi', 'Delhi', '499277',
             'medium', 530090.60,
             'note_verify',
             NOW() - interval '52 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '30bcad88-764e-43ed-bb80-aba153f58f2d', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.465611, 17.457746), 4326),
             'Telangana', 'Hyderabad', '518302',
             'medium', 115195.54,
             'scam_sentinel',
             NOW() - interval '151 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '74927c47-c79c-4a35-982e-1d4b866c0340', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.791992, 18.999229), 4326),
             'Maharashtra', 'Mumbai', '498424',
             'low', 245552.22,
             'scam_sentinel',
             NOW() - interval '281 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '847fd854-7252-4d06-a9c8-9addde516c97', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.41759, 17.495608), 4326),
             'Telangana', 'Hyderabad', '584681',
             'high', 51334.84,
             'fraud_graph',
             NOW() - interval '311 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '418f598a-554b-4527-9c67-ae4905f70a4f', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.370252, 17.331421), 4326),
             'Telangana', 'Hyderabad', '507290',
             'critical', 1047309.07,
             'citizen_shield',
             NOW() - interval '339 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '0baa7baf-f0b6-44b3-9cd7-a2e53056c9f9', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.780423, 18.990268), 4326),
             'Maharashtra', 'Mumbai', '528699',
             'medium', 234616.95,
             'citizen_shield',
             NOW() - interval '2 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '10a6c7d2-191f-4f38-a0cf-f07da9aea227', 'phishing',
             'Phishing reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.214808, 28.582474), 4326),
             'Delhi', 'Delhi', '425424',
             'medium', 43474.86,
             'fraud_graph',
             NOW() - interval '327 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'edd593ea-394e-4580-9e76-3d8b2b71946a', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.947192, 18.931136), 4326),
             'Maharashtra', 'Mumbai', '523455',
             'high', 736199.73,
             'citizen_shield',
             NOW() - interval '47 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '9ac79b25-6f2b-4edd-8190-455e7b07e13e', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.574204, 12.946882), 4326),
             'Karnataka', 'Bangalore', '516857',
             'medium', 71702.30,
             'note_verify',
             NOW() - interval '239 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '5db6d62d-d147-4cb1-864f-18b795589db7', 'upi_fraud',
             'Upi Fraud reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.888492, 19.21809), 4326),
             'Maharashtra', 'Mumbai', '574972',
             'high', 149570.42,
             'citizen_shield',
             NOW() - interval '278 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '46dfee2e-59c8-4bc5-a5c2-66df542e4ca2', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.041005, 28.711808), 4326),
             'Delhi', 'Delhi', '536991',
             'high', 630854.95,
             'note_verify',
             NOW() - interval '294 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '4f6cc266-d569-4652-9d41-27677f3e0ba7', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.365791, 17.395252), 4326),
             'Telangana', 'Hyderabad', '549741',
             'low', 1351180.32,
             'fraud_graph',
             NOW() - interval '62 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'c0e1dc41-81d0-450a-8dab-6f56c430a73f', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.539812, 17.389808), 4326),
             'Telangana', 'Hyderabad', '450521',
             'critical', 193648.07,
             'note_verify',
             NOW() - interval '41 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '9c265877-8587-404f-85e5-9145ca36eadd', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.549454, 17.387079), 4326),
             'Telangana', 'Hyderabad', '555988',
             'low', 390540.11,
             'scam_sentinel',
             NOW() - interval '45 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '77dd61df-6e5a-43dd-8bb4-8d4f6abcf112', 'ficn_seizure',
             'Ficn Seizure reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.080451, 28.611259), 4326),
             'Delhi', 'Delhi', '403241',
             'medium', 1180893.21,
             'note_verify',
             NOW() - interval '58 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '99f171a1-0278-4d8d-a87b-902cfef3039d', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.185174, 28.541496), 4326),
             'Delhi', 'Delhi', '547504',
             'critical', 1170419.32,
             'citizen_shield',
             NOW() - interval '275 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'f71a6096-6378-44d6-adda-4b042203400d', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.402827, 17.475579), 4326),
             'Telangana', 'Hyderabad', '559635',
             'medium', 712204.69,
             'fraud_graph',
             NOW() - interval '142 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '5fbb63da-62c2-4e05-abca-0f444de67fb3', 'investment_scam',
             'Investment Scam reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.222325, 28.673108), 4326),
             'Delhi', 'Delhi', '486899',
             'low', 1037318.06,
             'scam_sentinel',
             NOW() - interval '244 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '8d3efc33-3bed-4858-aace-1bbd2cdfa56f', 'ficn_seizure',
             'Ficn Seizure reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.354047, 17.479406), 4326),
             'Telangana', 'Hyderabad', '528875',
             'medium', 1288061.00,
             'scam_sentinel',
             NOW() - interval '117 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'ff6ef004-d6d7-46b7-a56c-6cb71460cc67', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.863053, 19.270203), 4326),
             'Maharashtra', 'Mumbai', '509254',
             'medium', 909443.80,
             'scam_sentinel',
             NOW() - interval '97 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '40d34654-501a-4908-bb1f-b8e33cce349f', 'investment_scam',
             'Investment Scam reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.112868, 28.755761), 4326),
             'Delhi', 'Delhi', '498018',
             'high', 1232421.00,
             'fraud_graph',
             NOW() - interval '34 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7b0a06d2-18bf-430c-8f28-aab740fd0363', 'phishing',
             'Phishing reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.00426, 28.641903), 4326),
             'Delhi', 'Delhi', '407588',
             'high', 264737.35,
             'fraud_graph',
             NOW() - interval '30 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a515ec09-0182-43ae-baf0-36b5675d6ebe', 'other',
             'Other reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.962787, 19.07345), 4326),
             'Maharashtra', 'Mumbai', '496561',
             'low', 1236141.91,
             'note_verify',
             NOW() - interval '326 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '20f5d65c-bf67-4aea-b779-6adaeb09fc1b', 'investment_scam',
             'Investment Scam reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.398388, 17.436235), 4326),
             'Telangana', 'Hyderabad', '446552',
             'medium', 1440977.97,
             'note_verify',
             NOW() - interval '301 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '91cf0e3c-5ba8-419b-b627-fdebab9c51c3', 'ficn_seizure',
             'Ficn Seizure reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.285062, 28.59639), 4326),
             'Delhi', 'Delhi', '580578',
             'high', 140135.92,
             'scam_sentinel',
             NOW() - interval '198 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b0cc689f-9d93-4c8f-8fc6-07a49d4fc623', 'upi_fraud',
             'Upi Fraud reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.933764, 19.224452), 4326),
             'Maharashtra', 'Mumbai', '569706',
             'high', 341542.50,
             'fraud_graph',
             NOW() - interval '138 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a3126edf-a3fa-4f1b-b1d4-fc9e982f22bd', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.672926, 12.97832), 4326),
             'Karnataka', 'Bangalore', '434685',
             'low', 972820.47,
             'scam_sentinel',
             NOW() - interval '115 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '0c141780-ef44-4e5e-8498-a314df9e9286', 'other',
             'Other reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.834147, 19.205933), 4326),
             'Maharashtra', 'Mumbai', '511098',
             'high', 1343747.05,
             'citizen_shield',
             NOW() - interval '236 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '83d6ebad-1e1d-48b9-9ed5-df392c9759a3', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.912211, 19.077345), 4326),
             'Maharashtra', 'Mumbai', '426820',
             'medium', 15984.62,
             'citizen_shield',
             NOW() - interval '288 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '60cef311-efa5-4fd0-9dbc-95699b702c8e', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.559695, 13.002263), 4326),
             'Karnataka', 'Bangalore', '488154',
             'medium', 1482599.64,
             'citizen_shield',
             NOW() - interval '142 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '5444df4e-4aef-4a2f-95ae-9486326b4c56', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.957398, 19.170216), 4326),
             'Maharashtra', 'Mumbai', '535605',
             'low', 1149384.21,
             'scam_sentinel',
             NOW() - interval '308 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '9d6a495d-d8a4-4383-b096-d056f328612c', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.005972, 28.589484), 4326),
             'Delhi', 'Delhi', '477490',
             'high', 392842.28,
             'note_verify',
             NOW() - interval '208 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'edbf20bc-6d75-490e-9368-0e0fc01d6157', 'phishing',
             'Phishing reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.233228, 28.509889), 4326),
             'Delhi', 'Delhi', '489959',
             'high', 1091192.07,
             'fraud_graph',
             NOW() - interval '352 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '25e63393-d20c-4e8e-a9fa-1324447ad4e2', 'other',
             'Other reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.312611, 28.719771), 4326),
             'Delhi', 'Delhi', '478694',
             'medium', 1268901.77,
             'fraud_graph',
             NOW() - interval '151 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '4e0930f5-6c8e-4097-a6ba-a64741acbc82', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.824317, 18.948619), 4326),
             'Maharashtra', 'Mumbai', '447990',
             'high', 1420650.45,
             'citizen_shield',
             NOW() - interval '336 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'c1a1ccf1-1ea5-4046-ace8-ea64171c5f01', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.926284, 19.035008), 4326),
             'Maharashtra', 'Mumbai', '486852',
             'medium', 560665.23,
             'citizen_shield',
             NOW() - interval '238 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '2a6dd855-903d-45bd-9640-58ad94144f2e', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.523279, 17.394107), 4326),
             'Telangana', 'Hyderabad', '562700',
             'medium', 111467.53,
             'fraud_graph',
             NOW() - interval '257 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '45ba7285-c119-459e-a4a0-924c974025b5', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.881266, 19.158665), 4326),
             'Maharashtra', 'Mumbai', '439525',
             'low', 210361.06,
             'fraud_graph',
             NOW() - interval '176 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '55daa9b2-bdf8-4903-bcb4-a61d442ede8f', 'investment_scam',
             'Investment Scam reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.312648, 28.659433), 4326),
             'Delhi', 'Delhi', '587608',
             'low', 274633.37,
             'scam_sentinel',
             NOW() - interval '250 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7ab496c5-dfc2-4438-b2ba-bb3f6f2047f4', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.075366, 28.776259), 4326),
             'Delhi', 'Delhi', '471703',
             'low', 318026.64,
             'fraud_graph',
             NOW() - interval '296 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '0b4eb471-89bf-41a6-898f-cf6e621f63e0', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.652714, 12.972394), 4326),
             'Karnataka', 'Bangalore', '513694',
             'low', 952063.87,
             'note_verify',
             NOW() - interval '220 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b37cf01c-a629-47b1-87bb-d0667babd592', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.357545, 17.376663), 4326),
             'Telangana', 'Hyderabad', '403690',
             'high', 1338549.56,
             'fraud_graph',
             NOW() - interval '10 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '4116984b-3a27-4c45-8a5b-699fd99e9806', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.549765, 13.006672), 4326),
             'Karnataka', 'Bangalore', '481813',
             'high', 197751.55,
             'note_verify',
             NOW() - interval '258 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '585d912a-2c46-4f5a-9198-b35e56423943', 'ficn_seizure',
             'Ficn Seizure reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.664769, 12.891755), 4326),
             'Karnataka', 'Bangalore', '519518',
             'critical', 1093108.71,
             'citizen_shield',
             NOW() - interval '223 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '0d353a77-6e09-48fc-825d-c3aa93769657', 'investment_scam',
             'Investment Scam reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.418547, 17.499094), 4326),
             'Telangana', 'Hyderabad', '449394',
             'medium', 251500.85,
             'note_verify',
             NOW() - interval '10 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd83bb1c2-30d1-4c3f-8ef5-ac4079041591', 'other',
             'Other reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.797553, 19.176324), 4326),
             'Maharashtra', 'Mumbai', '532286',
             'low', 257632.19,
             'citizen_shield',
             NOW() - interval '365 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a20d70db-74ca-4864-964c-21f9b9044c0c', 'ficn_seizure',
             'Ficn Seizure reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.675309, 12.859341), 4326),
             'Karnataka', 'Bangalore', '563351',
             'high', 77637.51,
             'scam_sentinel',
             NOW() - interval '339 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd264457b-fde6-4dc6-a8fa-82afe9bd41f2', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.780129, 19.217726), 4326),
             'Maharashtra', 'Mumbai', '499681',
             'medium', 189774.62,
             'citizen_shield',
             NOW() - interval '243 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '637e9fff-fb3d-48f9-8619-6744c2c75b58', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.637148, 12.901374), 4326),
             'Karnataka', 'Bangalore', '573451',
             'medium', 155964.87,
             'citizen_shield',
             NOW() - interval '319 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'ca07eb40-d6cb-4bb0-829a-c65997dadcc8', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.666131, 12.884291), 4326),
             'Karnataka', 'Bangalore', '561925',
             'medium', 181013.18,
             'scam_sentinel',
             NOW() - interval '55 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '2c107faf-0fef-4962-be5c-945b519a3ec3', 'phishing',
             'Phishing reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.261184, 28.670521), 4326),
             'Delhi', 'Delhi', '493827',
             'critical', 1056637.94,
             'citizen_shield',
             NOW() - interval '83 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '2e91a7bc-8083-49cb-9c1b-ed4295672b30', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.813616, 19.088615), 4326),
             'Maharashtra', 'Mumbai', '400717',
             'medium', 24060.35,
             'scam_sentinel',
             NOW() - interval '57 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '81f7c7df-3f6c-4c52-9530-05c4edd7aaae', 'digital_arrest',
             'Digital Arrest reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.379829, 17.433804), 4326),
             'Telangana', 'Hyderabad', '419673',
             'high', 1086727.61,
             'scam_sentinel',
             NOW() - interval '132 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd7cb6295-1baa-417d-a73b-2e160d1fd015', 'ficn_seizure',
             'Ficn Seizure reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.695458, 12.964188), 4326),
             'Karnataka', 'Bangalore', '426164',
             'medium', 1220701.73,
             'scam_sentinel',
             NOW() - interval '149 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '575cd163-db1c-4cbb-8c38-bed0d26e65bf', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.120398, 28.689495), 4326),
             'Delhi', 'Delhi', '598758',
             'low', 1335986.56,
             'scam_sentinel',
             NOW() - interval '71 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'f06fba4b-c3f0-4d47-b698-ae733a9313a7', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.571505, 12.892628), 4326),
             'Karnataka', 'Bangalore', '470335',
             'critical', 1318320.93,
             'scam_sentinel',
             NOW() - interval '191 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '470cd105-d46d-4787-963b-ca3d9b9d160c', 'investment_scam',
             'Investment Scam reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.430156, 17.336574), 4326),
             'Telangana', 'Hyderabad', '501113',
             'medium', 1036404.13,
             'note_verify',
             NOW() - interval '216 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'f207704d-d850-4a57-979b-6ec012b8cde2', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.522611, 13.049227), 4326),
             'Karnataka', 'Bangalore', '441784',
             'high', 160051.09,
             'note_verify',
             NOW() - interval '292 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7989ff6d-965c-4021-99b1-3a5ee2612f1a', 'ficn_seizure',
             'Ficn Seizure reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.57595, 12.895315), 4326),
             'Karnataka', 'Bangalore', '579428',
             'high', 1320525.62,
             'fraud_graph',
             NOW() - interval '248 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '36dc5a36-7707-4a91-a955-525c22b92c3c', 'digital_arrest',
             'Digital Arrest reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.432257, 17.322587), 4326),
             'Telangana', 'Hyderabad', '571697',
             'low', 474785.73,
             'fraud_graph',
             NOW() - interval '343 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '0b6af407-303e-4350-b669-176fc12a9441', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.487648, 17.40382), 4326),
             'Telangana', 'Hyderabad', '573464',
             'low', 1091344.69,
             'note_verify',
             NOW() - interval '178 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '03ef9983-abdb-4252-b0dc-0b0969711045', 'phishing',
             'Phishing reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.529731, 13.010351), 4326),
             'Karnataka', 'Bangalore', '560671',
             'high', 86576.34,
             'fraud_graph',
             NOW() - interval '259 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '03c5fda4-c8ac-4ba6-ae3b-6d81fdae960c', 'digital_arrest',
             'Digital Arrest reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.523883, 17.470374), 4326),
             'Telangana', 'Hyderabad', '484052',
             'high', 365133.27,
             'citizen_shield',
             NOW() - interval '26 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '786c2e25-d54a-4f64-ba5f-1df1051fb784', 'upi_fraud',
             'Upi Fraud reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.101455, 28.654139), 4326),
             'Delhi', 'Delhi', '516441',
             'low', 1202885.63,
             'note_verify',
             NOW() - interval '46 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'ece5a2d5-f0f5-4da9-830d-597d0886d54e', 'investment_scam',
             'Investment Scam reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.373741, 17.389414), 4326),
             'Telangana', 'Hyderabad', '404658',
             'high', 158451.77,
             'note_verify',
             NOW() - interval '19 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd9afd434-ba70-4c8e-86f6-496b1dd991df', 'phishing',
             'Phishing reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(76.986358, 28.500048), 4326),
             'Delhi', 'Delhi', '567126',
             'critical', 460373.95,
             'fraud_graph',
             NOW() - interval '336 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '15b41ec2-26fa-44ef-8850-64c1deb03f5d', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.572668, 13.087589), 4326),
             'Karnataka', 'Bangalore', '519133',
             'high', 501299.08,
             'note_verify',
             NOW() - interval '337 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'aff065fb-6032-43a5-a44b-50c3e3e1b088', 'other',
             'Other reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(76.988975, 28.626709), 4326),
             'Delhi', 'Delhi', '489484',
             'medium', 535932.77,
             'citizen_shield',
             NOW() - interval '281 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a4cf833e-0c2f-4641-990a-570ddb0b1974', 'upi_fraud',
             'Upi Fraud reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(76.968311, 28.696587), 4326),
             'Delhi', 'Delhi', '587919',
             'medium', 1115053.78,
             'note_verify',
             NOW() - interval '55 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '627107ba-ecc5-4659-a1d8-e406f682a509', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.795357, 18.97445), 4326),
             'Maharashtra', 'Mumbai', '449959',
             'medium', 1076597.93,
             'scam_sentinel',
             NOW() - interval '213 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '6169a9f4-0fcf-4c96-81b7-1c8c9b18ca41', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.91115, 19.140631), 4326),
             'Maharashtra', 'Mumbai', '518097',
             'high', 688794.88,
             'fraud_graph',
             NOW() - interval '256 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd61d9d18-1b1c-4266-bfe3-3a86e033703c', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.886178, 19.179761), 4326),
             'Maharashtra', 'Mumbai', '526597',
             'high', 1386934.46,
             'fraud_graph',
             NOW() - interval '355 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '53bc33fe-cd54-4949-81a0-e66631c4812b', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.525676, 13.032624), 4326),
             'Karnataka', 'Bangalore', '558901',
             'high', 1324630.32,
             'note_verify',
             NOW() - interval '215 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '16715cc6-579f-4dc7-b970-43c52e1494ab', 'ficn_seizure',
             'Ficn Seizure reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.502475, 17.483182), 4326),
             'Telangana', 'Hyderabad', '489878',
             'medium', 1455885.02,
             'note_verify',
             NOW() - interval '69 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'af1ffa3f-cdc2-4c43-a5ba-5bb5bdf1f6c3', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.956152, 19.128959), 4326),
             'Maharashtra', 'Mumbai', '583892',
             'medium', 823969.93,
             'citizen_shield',
             NOW() - interval '365 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '94400927-9e99-49d5-86a5-9b76717f8e54', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.543469, 12.988395), 4326),
             'Karnataka', 'Bangalore', '476173',
             'high', 1031483.89,
             'fraud_graph',
             NOW() - interval '364 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd1767a53-6607-46b4-ad18-c7fb0753c3ff', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.600779, 13.089582), 4326),
             'Karnataka', 'Bangalore', '586214',
             'high', 177530.85,
             'citizen_shield',
             NOW() - interval '288 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '2162a08b-4fa7-4ac4-bf8e-53d60269a4f4', 'investment_scam',
             'Investment Scam reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.216863, 28.659779), 4326),
             'Delhi', 'Delhi', '539959',
             'high', 432462.33,
             'note_verify',
             NOW() - interval '7 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '13dac6f3-ec2c-4af6-ad52-acdc2a243454', 'other',
             'Other reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.008131, 28.507076), 4326),
             'Delhi', 'Delhi', '469986',
             'low', 1126526.60,
             'fraud_graph',
             NOW() - interval '147 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'e380b43b-e766-49ac-bf77-d93148483246', 'ficn_seizure',
             'Ficn Seizure reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.512407, 12.886607), 4326),
             'Karnataka', 'Bangalore', '541865',
             'medium', 53298.04,
             'note_verify',
             NOW() - interval '53 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '2cba6fe5-c3a5-46e1-8590-88ab2b7fe14d', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.612377, 13.018882), 4326),
             'Karnataka', 'Bangalore', '547133',
             'high', 586385.56,
             'citizen_shield',
             NOW() - interval '355 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'e64cd375-3ada-46c2-bfac-7eb4ee2e6350', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.577511, 13.081621), 4326),
             'Karnataka', 'Bangalore', '544736',
             'medium', 85434.28,
             'citizen_shield',
             NOW() - interval '104 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'c8dd16fa-d51a-49f1-9d4c-aab68d1f02fc', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.674024, 13.045231), 4326),
             'Karnataka', 'Bangalore', '584714',
             'critical', 1065770.45,
             'citizen_shield',
             NOW() - interval '302 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '198b8054-41cf-4f4e-a502-13e72caba068', 'upi_fraud',
             'Upi Fraud reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.260459, 28.668948), 4326),
             'Delhi', 'Delhi', '446511',
             'medium', 1475262.72,
             'scam_sentinel',
             NOW() - interval '96 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '6b2c328d-cd9a-4df7-a747-74f9288bddc8', 'digital_arrest',
             'Digital Arrest reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.373871, 17.447016), 4326),
             'Telangana', 'Hyderabad', '545908',
             'medium', 400038.19,
             'fraud_graph',
             NOW() - interval '300 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '5adb4717-46b0-43bc-80b0-bcad57b2d4bd', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.443266, 17.301129), 4326),
             'Telangana', 'Hyderabad', '484575',
             'low', 897336.10,
             'citizen_shield',
             NOW() - interval '252 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '09533d8c-1c22-471f-ad73-49a112bb2fe7', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.364576, 17.410032), 4326),
             'Telangana', 'Hyderabad', '457661',
             'medium', 1435696.64,
             'scam_sentinel',
             NOW() - interval '259 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'ab13b259-bad9-4713-9ba8-ccc3e8b88a10', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.854718, 19.10637), 4326),
             'Maharashtra', 'Mumbai', '455929',
             'medium', 996685.04,
             'citizen_shield',
             NOW() - interval '185 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '92dbe91b-afea-43db-b07a-b16b7b11d171', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.899839, 19.261117), 4326),
             'Maharashtra', 'Mumbai', '597167',
             'critical', 1471794.13,
             'scam_sentinel',
             NOW() - interval '59 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '66230266-e336-4c09-9a12-d0ce91176906', 'phishing',
             'Phishing reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.680899, 12.961417), 4326),
             'Karnataka', 'Bangalore', '463917',
             'critical', 1438550.74,
             'citizen_shield',
             NOW() - interval '196 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'c2b441d0-232a-45f1-b9d4-8a08f88727fc', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.427175, 17.488998), 4326),
             'Telangana', 'Hyderabad', '406476',
             'high', 1367447.21,
             'citizen_shield',
             NOW() - interval '264 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '422b2e1f-4c6a-42a5-9bea-12a30ad4f1ac', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.35877, 17.389111), 4326),
             'Telangana', 'Hyderabad', '534714',
             'low', 128106.44,
             'scam_sentinel',
             NOW() - interval '86 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b6fdfadc-b3e0-4f3a-842e-31ea3e738807', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.456641, 17.454664), 4326),
             'Telangana', 'Hyderabad', '575724',
             'low', 946124.15,
             'fraud_graph',
             NOW() - interval '351 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'e3c932a3-6990-4811-a5e7-0132a60ed2c7', 'other',
             'Other reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.165102, 28.5291), 4326),
             'Delhi', 'Delhi', '594347',
             'high', 1163934.08,
             'scam_sentinel',
             NOW() - interval '352 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd4574b98-b8f8-4291-ad74-448d5cd6ba5f', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.83966, 19.074506), 4326),
             'Maharashtra', 'Mumbai', '446659',
             'low', 1192351.11,
             'scam_sentinel',
             NOW() - interval '295 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '53507494-4255-410e-ac4d-b25c34ac4ece', 'investment_scam',
             'Investment Scam reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.431527, 17.482197), 4326),
             'Telangana', 'Hyderabad', '513514',
             'high', 478024.35,
             'note_verify',
             NOW() - interval '345 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '71b55043-5069-4e26-9f35-a905ca8a3e86', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.92126, 18.902242), 4326),
             'Maharashtra', 'Mumbai', '553513',
             'high', 73047.70,
             'scam_sentinel',
             NOW() - interval '184 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '15b258cb-57d3-4243-a3eb-0b1a71f1ed96', 'ficn_seizure',
             'Ficn Seizure reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.507378, 17.321227), 4326),
             'Telangana', 'Hyderabad', '473798',
             'high', 1149084.99,
             'note_verify',
             NOW() - interval '196 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '916e4441-4904-494b-aee2-1c6e19f29f67', 'phishing',
             'Phishing reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.139595, 28.685002), 4326),
             'Delhi', 'Delhi', '595757',
             'medium', 589533.89,
             'citizen_shield',
             NOW() - interval '325 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7ebfdd05-240e-4be9-a354-bea78923963b', 'other',
             'Other reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.961975, 19.15737), 4326),
             'Maharashtra', 'Mumbai', '402922',
             'high', 832518.66,
             'fraud_graph',
             NOW() - interval '64 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '45cd729c-6ad2-4b5d-af52-8fc775403c80', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.852757, 19.117633), 4326),
             'Maharashtra', 'Mumbai', '479872',
             'critical', 319029.07,
             'citizen_shield',
             NOW() - interval '109 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '0e5295f4-c92d-41df-98b2-15db554c8d43', 'upi_fraud',
             'Upi Fraud reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.155021, 28.680861), 4326),
             'Delhi', 'Delhi', '561712',
             'low', 1252948.81,
             'fraud_graph',
             NOW() - interval '59 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '5bce5783-9766-4e7a-8aa5-e442c1d56de4', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.948973, 19.203871), 4326),
             'Maharashtra', 'Mumbai', '544091',
             'medium', 114351.14,
             'scam_sentinel',
             NOW() - interval '129 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a31642d2-507d-496b-897c-ee459bfcee2c', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.87231, 19.175724), 4326),
             'Maharashtra', 'Mumbai', '575976',
             'medium', 984932.11,
             'scam_sentinel',
             NOW() - interval '146 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '22b715c5-dd7d-494c-9c24-a156f7a251ea', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.563557, 13.07503), 4326),
             'Karnataka', 'Bangalore', '572863',
             'medium', 461984.86,
             'fraud_graph',
             NOW() - interval '290 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'cdb9d084-4549-4380-b715-e412ea09a1ac', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.691732, 13.051925), 4326),
             'Karnataka', 'Bangalore', '464533',
             'low', 1179561.87,
             'note_verify',
             NOW() - interval '142 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'cce4f0ab-e8c6-4a52-97d9-de387e121e8d', 'investment_scam',
             'Investment Scam reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.496595, 17.326861), 4326),
             'Telangana', 'Hyderabad', '494041',
             'medium', 1163276.61,
             'note_verify',
             NOW() - interval '283 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '6c89221d-c62c-440d-a087-12e215dc4780', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.787214, 19.14531), 4326),
             'Maharashtra', 'Mumbai', '436700',
             'high', 1337489.07,
             'fraud_graph',
             NOW() - interval '135 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '13c525c9-214d-40b7-9d16-1da7dc94dcc7', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.645485, 13.006655), 4326),
             'Karnataka', 'Bangalore', '565577',
             'high', 51635.38,
             'note_verify',
             NOW() - interval '303 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '92904773-560f-4173-80cb-71689482ff01', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.824729, 18.913929), 4326),
             'Maharashtra', 'Mumbai', '438963',
             'medium', 551898.85,
             'fraud_graph',
             NOW() - interval '302 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '82acc237-da93-45c5-b8ad-4e6a2f9f522a', 'phishing',
             'Phishing reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.59294, 12.92275), 4326),
             'Karnataka', 'Bangalore', '495385',
             'low', 755740.07,
             'fraud_graph',
             NOW() - interval '315 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '721902a6-9057-456c-8ca4-ecbc97411e26', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.528074, 13.039302), 4326),
             'Karnataka', 'Bangalore', '548324',
             'low', 990822.89,
             'fraud_graph',
             NOW() - interval '248 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '37225f08-4cc7-44f1-b8cf-9f5102f005d6', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.502294, 17.308084), 4326),
             'Telangana', 'Hyderabad', '496845',
             'low', 354857.91,
             'fraud_graph',
             NOW() - interval '266 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '941f5e67-97ad-4574-a054-0782e8ae3580', 'investment_scam',
             'Investment Scam reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.443935, 17.37225), 4326),
             'Telangana', 'Hyderabad', '410460',
             'high', 1470981.72,
             'citizen_shield',
             NOW() - interval '53 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7718f339-1a30-40c6-8528-f57bdfab2315', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.665929, 12.980343), 4326),
             'Karnataka', 'Bangalore', '542698',
             'medium', 857389.43,
             'note_verify',
             NOW() - interval '335 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b30e9fe1-daa2-45b9-9755-86c52e8469c1', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.309291, 28.66455), 4326),
             'Delhi', 'Delhi', '498652',
             'medium', 1459147.79,
             'fraud_graph',
             NOW() - interval '265 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '2416f73d-ac16-4450-9b84-7e28966dd51a', 'investment_scam',
             'Investment Scam reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.088013, 28.728826), 4326),
             'Delhi', 'Delhi', '401729',
             'high', 755246.29,
             'fraud_graph',
             NOW() - interval '226 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '6a2d6fba-7916-4d80-872f-6acb2db35a04', 'upi_fraud',
             'Upi Fraud reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.90513, 18.929294), 4326),
             'Maharashtra', 'Mumbai', '441250',
             'low', 546523.30,
             'scam_sentinel',
             NOW() - interval '339 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '23d65c51-fc4a-434c-8180-fba3d90c49da', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.921254, 19.208246), 4326),
             'Maharashtra', 'Mumbai', '525572',
             'high', 320002.41,
             'fraud_graph',
             NOW() - interval '332 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '09854a4b-42d5-4217-801c-e584fcad712c', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.358629, 17.304489), 4326),
             'Telangana', 'Hyderabad', '435317',
             'medium', 946162.94,
             'scam_sentinel',
             NOW() - interval '294 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '5d83e866-c918-4dea-b1d3-4d96dac59790', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.963714, 18.96321), 4326),
             'Maharashtra', 'Mumbai', '557117',
             'critical', 1454019.31,
             'scam_sentinel',
             NOW() - interval '339 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'aea883b9-e003-4d8b-bfdd-8222e921257a', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.393319, 17.489451), 4326),
             'Telangana', 'Hyderabad', '526266',
             'critical', 259997.34,
             'note_verify',
             NOW() - interval '308 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd6191b27-823f-4b97-bfb7-6ddc00d201fd', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.931173, 19.121406), 4326),
             'Maharashtra', 'Mumbai', '469342',
             'high', 255743.94,
             'citizen_shield',
             NOW() - interval '233 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a3c5f1d6-ba3c-4eed-b5f9-c561901d0cd7', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.575642, 12.867211), 4326),
             'Karnataka', 'Bangalore', '453044',
             'low', 786453.46,
             'note_verify',
             NOW() - interval '77 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'c20f7480-2f30-4f97-a180-6b1efa954634', 'phishing',
             'Phishing reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.680322, 12.894356), 4326),
             'Karnataka', 'Bangalore', '539311',
             'low', 757477.17,
             'scam_sentinel',
             NOW() - interval '48 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'dc57b551-e593-4c28-9a0a-4bb0dc193091', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.19139, 28.536492), 4326),
             'Delhi', 'Delhi', '577880',
             'high', 975601.44,
             'note_verify',
             NOW() - interval '190 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b6217f99-d063-4af6-9c57-3dcfe9063a2a', 'investment_scam',
             'Investment Scam reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.435791, 17.439529), 4326),
             'Telangana', 'Hyderabad', '499938',
             'high', 529024.13,
             'scam_sentinel',
             NOW() - interval '218 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '6936e2e6-9323-420f-b874-bdc98110cf05', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.818828, 19.081314), 4326),
             'Maharashtra', 'Mumbai', '542535',
             'medium', 615926.82,
             'fraud_graph',
             NOW() - interval '3 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'ca3072a4-2409-4a36-b5c5-10fddee111cc', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.615597, 13.047356), 4326),
             'Karnataka', 'Bangalore', '498311',
             'medium', 983546.45,
             'citizen_shield',
             NOW() - interval '210 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a826b52d-a014-490f-9e44-4c0b66d63287', 'ficn_seizure',
             'Ficn Seizure reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.21063, 28.543338), 4326),
             'Delhi', 'Delhi', '540536',
             'medium', 638224.51,
             'citizen_shield',
             NOW() - interval '314 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd7fa3475-7435-429c-9fbc-9d1687c1d042', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.928544, 19.15863), 4326),
             'Maharashtra', 'Mumbai', '546161',
             'medium', 726289.30,
             'citizen_shield',
             NOW() - interval '287 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '1a895508-14bc-4d00-aaab-4c1e92ae3e52', 'ficn_seizure',
             'Ficn Seizure reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.072661, 28.571058), 4326),
             'Delhi', 'Delhi', '504367',
             'high', 1104994.73,
             'scam_sentinel',
             NOW() - interval '118 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd6ad7ac3-100b-4176-8790-dbb2df0ce3f5', 'upi_fraud',
             'Upi Fraud reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.014718, 28.695807), 4326),
             'Delhi', 'Delhi', '488719',
             'medium', 1202276.33,
             'scam_sentinel',
             NOW() - interval '83 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '77099f84-af0c-4f2e-b0e1-4a37968ab501', 'upi_fraud',
             'Upi Fraud reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.271748, 28.678045), 4326),
             'Delhi', 'Delhi', '557350',
             'medium', 655889.26,
             'scam_sentinel',
             NOW() - interval '135 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '6e802d14-3697-4f75-8a6d-f388103897ca', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.777929, 18.930415), 4326),
             'Maharashtra', 'Mumbai', '505026',
             'critical', 922878.56,
             'citizen_shield',
             NOW() - interval '365 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '38c91fc6-5add-406b-8cf0-fb491569f3c7', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.504722, 17.311493), 4326),
             'Telangana', 'Hyderabad', '515073',
             'high', 21012.04,
             'citizen_shield',
             NOW() - interval '100 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '4edc6108-a5c8-4045-a973-fa6a699ca1d2', 'upi_fraud',
             'Upi Fraud reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.878321, 19.127816), 4326),
             'Maharashtra', 'Mumbai', '576691',
             'high', 58911.39,
             'fraud_graph',
             NOW() - interval '336 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '1d39a26e-0b64-4daf-99f5-5770db50550c', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.979332, 18.959829), 4326),
             'Maharashtra', 'Mumbai', '503584',
             'medium', 611149.20,
             'fraud_graph',
             NOW() - interval '266 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '26363049-574a-44d2-b666-32c8ed63ca85', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.963027, 19.167376), 4326),
             'Maharashtra', 'Mumbai', '546568',
             'medium', 1372938.42,
             'citizen_shield',
             NOW() - interval '178 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '03214dde-8774-4da6-a349-cb299cfe3c31', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.471273, 17.355302), 4326),
             'Telangana', 'Hyderabad', '505894',
             'medium', 864485.55,
             'citizen_shield',
             NOW() - interval '90 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '9012eaed-c6a1-489b-b30d-37390c9f8f71', 'ficn_seizure',
             'Ficn Seizure reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(76.978954, 28.52981), 4326),
             'Delhi', 'Delhi', '430673',
             'medium', 1205398.65,
             'citizen_shield',
             NOW() - interval '276 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b55f0288-b159-4c94-bf5c-8e15132ed9a9', 'investment_scam',
             'Investment Scam reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.488838, 17.414979), 4326),
             'Telangana', 'Hyderabad', '463772',
             'medium', 1137422.56,
             'note_verify',
             NOW() - interval '349 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '9382c338-f202-4873-83d8-9116442f0b3f', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(76.96094, 28.664311), 4326),
             'Delhi', 'Delhi', '500315',
             'medium', 952324.39,
             'fraud_graph',
             NOW() - interval '347 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '8b5a2e83-d914-4a8f-b01c-68293ea08f4d', 'ficn_seizure',
             'Ficn Seizure reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.582485, 13.05004), 4326),
             'Karnataka', 'Bangalore', '402548',
             'medium', 1052723.74,
             'citizen_shield',
             NOW() - interval '128 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '60eb73f8-04c1-4543-a7c0-b33d27c26641', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.927246, 19.051594), 4326),
             'Maharashtra', 'Mumbai', '446788',
             'low', 717450.40,
             'citizen_shield',
             NOW() - interval '112 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a09f7dec-c84c-4418-a3d6-77a4c022a558', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.539424, 17.353815), 4326),
             'Telangana', 'Hyderabad', '449851',
             'critical', 751004.01,
             'fraud_graph',
             NOW() - interval '121 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '42457f1b-941e-4373-a8c8-a79a078ad2d4', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.541356, 13.068186), 4326),
             'Karnataka', 'Bangalore', '562161',
             'high', 537260.92,
             'scam_sentinel',
             NOW() - interval '62 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b9cd4a32-3560-4c2a-903c-ca998a381636', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.482685, 17.435162), 4326),
             'Telangana', 'Hyderabad', '541944',
             'low', 1437199.67,
             'note_verify',
             NOW() - interval '191 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '9c783685-6107-4773-9bef-b037ebc701be', 'phishing',
             'Phishing reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.697072, 12.973085), 4326),
             'Karnataka', 'Bangalore', '528661',
             'high', 278393.44,
             'citizen_shield',
             NOW() - interval '204 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '071081d4-91fa-4d77-b677-3a698766f30b', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.781371, 19.119133), 4326),
             'Maharashtra', 'Mumbai', '541759',
             'medium', 53681.16,
             'citizen_shield',
             NOW() - interval '202 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b7036e36-4f8b-4f59-a645-36318d15fb7f', 'digital_arrest',
             'Digital Arrest reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.441439, 17.455181), 4326),
             'Telangana', 'Hyderabad', '520604',
             'high', 476898.64,
             'scam_sentinel',
             NOW() - interval '7 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'cb4b929a-33aa-47f0-93e1-52d643bb5e1a', 'ficn_seizure',
             'Ficn Seizure reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.52015, 12.944857), 4326),
             'Karnataka', 'Bangalore', '468078',
             'high', 284792.90,
             'citizen_shield',
             NOW() - interval '122 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'ab9e46a7-9f93-4469-b3a6-93175899f21c', 'upi_fraud',
             'Upi Fraud reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.84205, 19.26424), 4326),
             'Maharashtra', 'Mumbai', '455189',
             'medium', 631543.95,
             'citizen_shield',
             NOW() - interval '187 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '772d01cb-9178-4a23-b8fa-c01d580f5614', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.385978, 17.355926), 4326),
             'Telangana', 'Hyderabad', '579833',
             'critical', 346707.29,
             'scam_sentinel',
             NOW() - interval '139 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '830b3800-69ef-4d22-bfd2-6d54bbc96b2f', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.521262, 17.411068), 4326),
             'Telangana', 'Hyderabad', '593604',
             'low', 228574.35,
             'scam_sentinel',
             NOW() - interval '91 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'fea3fd49-0d28-4b1e-8cb0-2195491a68a2', 'other',
             'Other reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.307308, 28.537652), 4326),
             'Delhi', 'Delhi', '588890',
             'medium', 477012.23,
             'note_verify',
             NOW() - interval '154 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '4c812618-aa9e-412d-bafb-6f195d48a60b', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.780019, 19.226231), 4326),
             'Maharashtra', 'Mumbai', '415738',
             'high', 327123.65,
             'citizen_shield',
             NOW() - interval '244 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '877af690-15b8-46ce-a30c-6c57df6d74e4', 'ficn_seizure',
             'Ficn Seizure reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.498919, 17.31926), 4326),
             'Telangana', 'Hyderabad', '546892',
             'medium', 838449.77,
             'citizen_shield',
             NOW() - interval '177 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '9cc9b92a-8953-46b0-9dd3-ee087a67a3d5', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.952147, 18.94607), 4326),
             'Maharashtra', 'Mumbai', '550967',
             'low', 976548.90,
             'fraud_graph',
             NOW() - interval '146 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '62589e24-899f-4081-b5fc-d89741667111', 'other',
             'Other reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.144997, 28.688494), 4326),
             'Delhi', 'Delhi', '420554',
             'medium', 574701.14,
             'citizen_shield',
             NOW() - interval '238 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'cca322be-a1eb-43fe-b898-169a0318e0c3', 'ficn_seizure',
             'Ficn Seizure reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.533515, 12.886212), 4326),
             'Karnataka', 'Bangalore', '560513',
             'medium', 859598.17,
             'scam_sentinel',
             NOW() - interval '41 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'ba7eba94-e12f-4889-9021-0a9eab98e434', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.836544, 18.986723), 4326),
             'Maharashtra', 'Mumbai', '558698',
             'high', 968743.22,
             'citizen_shield',
             NOW() - interval '228 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '87d530ec-e69c-4e21-a004-cda7c32fe269', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.499579, 17.487754), 4326),
             'Telangana', 'Hyderabad', '508524',
             'critical', 255140.57,
             'scam_sentinel',
             NOW() - interval '65 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '8d854757-9a88-4b97-b0a4-fb2cd4a5cf93', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.688087, 13.015506), 4326),
             'Karnataka', 'Bangalore', '455200',
             'high', 254531.15,
             'scam_sentinel',
             NOW() - interval '49 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '04d7683c-a933-41a5-a22f-9d3a7cba230c', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.885171, 19.233903), 4326),
             'Maharashtra', 'Mumbai', '537358',
             'high', 1148669.58,
             'scam_sentinel',
             NOW() - interval '54 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '938bb7b6-cdae-4722-b59e-c418f01fe581', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.907515, 18.959004), 4326),
             'Maharashtra', 'Mumbai', '464853',
             'medium', 1107701.88,
             'note_verify',
             NOW() - interval '321 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '2859f3b4-f9fd-4d92-ab61-82eb9da1b6b2', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.805828, 19.100162), 4326),
             'Maharashtra', 'Mumbai', '485249',
             'high', 1297040.51,
             'note_verify',
             NOW() - interval '277 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'ee7ce668-c2fa-4252-8f95-6381c22de06d', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.377023, 17.409709), 4326),
             'Telangana', 'Hyderabad', '554882',
             'medium', 898388.38,
             'note_verify',
             NOW() - interval '269 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'd48d5b6b-d0b6-47e5-9c9b-d18f0193dd78', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.681785, 12.983446), 4326),
             'Karnataka', 'Bangalore', '423476',
             'medium', 665581.16,
             'citizen_shield',
             NOW() - interval '212 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '214e047d-39ef-47aa-bc0f-9c2b0e626a49', 'upi_fraud',
             'Upi Fraud reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.770019, 19.015358), 4326),
             'Maharashtra', 'Mumbai', '522997',
             'medium', 804972.84,
             'note_verify',
             NOW() - interval '245 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7d1c22e8-6610-4f8d-ba7e-795088172f83', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.937573, 19.19103), 4326),
             'Maharashtra', 'Mumbai', '401892',
             'medium', 824577.23,
             'fraud_graph',
             NOW() - interval '211 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'cf80a97b-00a1-48dc-9492-7fcdf77ab8fe', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.399979, 17.387421), 4326),
             'Telangana', 'Hyderabad', '502163',
             'high', 1243498.15,
             'fraud_graph',
             NOW() - interval '135 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '1fd1a5e0-d7b4-4256-b2d0-9589d5597e15', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.878488, 19.137623), 4326),
             'Maharashtra', 'Mumbai', '579474',
             'high', 411438.35,
             'citizen_shield',
             NOW() - interval '212 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '2c5e7334-6018-4f30-9036-f27b4ebf22db', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.798691, 18.926016), 4326),
             'Maharashtra', 'Mumbai', '561934',
             'high', 681887.01,
             'note_verify',
             NOW() - interval '97 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '172cd15d-5800-4b34-afdc-fa99b2006d55', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.337886, 28.542602), 4326),
             'Delhi', 'Delhi', '426810',
             'low', 426761.23,
             'fraud_graph',
             NOW() - interval '225 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '6cedba00-e84b-465a-b20d-1c64c26a595f', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.530137, 12.908203), 4326),
             'Karnataka', 'Bangalore', '510164',
             'medium', 470807.14,
             'note_verify',
             NOW() - interval '191 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '99eb353e-a050-49e7-a80a-9a22eac197f0', 'upi_fraud',
             'Upi Fraud reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.082099, 28.721599), 4326),
             'Delhi', 'Delhi', '502871',
             'low', 111720.12,
             'note_verify',
             NOW() - interval '93 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '5b91b120-2d35-43f6-b9ee-a06cf81ed5e9', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.941623, 19.219785), 4326),
             'Maharashtra', 'Mumbai', '587349',
             'low', 377198.73,
             'note_verify',
             NOW() - interval '127 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '99f5b119-345e-4afd-bff7-a89962c445ac', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.592167, 12.858378), 4326),
             'Karnataka', 'Bangalore', '454643',
             'medium', 711874.19,
             'citizen_shield',
             NOW() - interval '166 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a2415089-43dc-436e-a705-ef56c2b87361', 'phishing',
             'Phishing reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.926392, 19.17673), 4326),
             'Maharashtra', 'Mumbai', '466404',
             'medium', 724438.24,
             'citizen_shield',
             NOW() - interval '102 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a08867d0-c226-4243-b359-db25bc032bc3', 'digital_arrest',
             'Digital Arrest reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.216678, 28.514585), 4326),
             'Delhi', 'Delhi', '513812',
             'medium', 490147.66,
             'fraud_graph',
             NOW() - interval '142 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '5998e296-7a6e-48b2-8d9a-089605ba83b8', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.548618, 12.948952), 4326),
             'Karnataka', 'Bangalore', '581076',
             'medium', 715529.66,
             'fraud_graph',
             NOW() - interval '191 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'e8d236b6-812c-4d0d-8fa6-7709987fa461', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.599984, 12.912181), 4326),
             'Karnataka', 'Bangalore', '599114',
             'high', 939572.83,
             'scam_sentinel',
             NOW() - interval '183 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '50718036-2a65-421f-93d2-374569e4d35d', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.658293, 13.025332), 4326),
             'Karnataka', 'Bangalore', '483031',
             'medium', 1472605.19,
             'citizen_shield',
             NOW() - interval '225 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a4fcac5f-d1c8-4439-a4c5-8df65e10456f', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.575554, 12.855338), 4326),
             'Karnataka', 'Bangalore', '410351',
             'low', 730526.69,
             'note_verify',
             NOW() - interval '287 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'aa33c5a7-f523-4501-89b3-61b0cac09397', 'upi_fraud',
             'Upi Fraud reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.809853, 19.164874), 4326),
             'Maharashtra', 'Mumbai', '484850',
             'medium', 1099941.60,
             'citizen_shield',
             NOW() - interval '307 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b74b32b0-2e17-45cb-b270-8ae012d49b59', 'upi_fraud',
             'Upi Fraud reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.363775, 17.410904), 4326),
             'Telangana', 'Hyderabad', '469035',
             'medium', 814700.90,
             'note_verify',
             NOW() - interval '1 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7959a140-14d7-41a9-9d86-368fc92c21f2', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.646732, 12.976489), 4326),
             'Karnataka', 'Bangalore', '495440',
             'high', 1165144.77,
             'fraud_graph',
             NOW() - interval '165 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'bd09f2e1-768c-4ab4-82df-acf55049f4c6', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.607791, 13.014572), 4326),
             'Karnataka', 'Bangalore', '579103',
             'low', 748835.99,
             'fraud_graph',
             NOW() - interval '314 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '9130a984-8b23-466d-9880-de5c88e6191f', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.837625, 19.055726), 4326),
             'Maharashtra', 'Mumbai', '417479',
             'medium', 70447.01,
             'fraud_graph',
             NOW() - interval '92 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'df96c06e-f424-4eae-b00a-502fab5bea15', 'digital_arrest',
             'Digital Arrest reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.447074, 17.340416), 4326),
             'Telangana', 'Hyderabad', '568231',
             'low', 1255267.79,
             'note_verify',
             NOW() - interval '270 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'fe3002ad-99e3-4fc0-9b69-8d3a78e9a199', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.509817, 12.997575), 4326),
             'Karnataka', 'Bangalore', '418579',
             'high', 24563.73,
             'fraud_graph',
             NOW() - interval '336 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'fab90611-e38e-4100-9bb8-44a73aa4d732', 'other',
             'Other reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(76.981983, 28.749135), 4326),
             'Delhi', 'Delhi', '546281',
             'low', 1116498.77,
             'note_verify',
             NOW() - interval '189 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '917ec2ef-6d11-4aa6-9774-39ffcb8f51b2', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.473387, 17.31166), 4326),
             'Telangana', 'Hyderabad', '418451',
             'low', 1252512.46,
             'scam_sentinel',
             NOW() - interval '111 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7a29b3d4-d4aa-43fc-860c-0cc35a1fdae1', 'phishing',
             'Phishing reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.495034, 17.319424), 4326),
             'Telangana', 'Hyderabad', '450625',
             'medium', 791657.07,
             'fraud_graph',
             NOW() - interval '292 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'c16f114d-7c54-4769-8c9c-2604a6ead5b0', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.649839, 12.894724), 4326),
             'Karnataka', 'Bangalore', '567411',
             'high', 866962.67,
             'note_verify',
             NOW() - interval '360 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'e881391b-cdba-4017-8326-d455bdd79590', 'upi_fraud',
             'Upi Fraud reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.533362, 13.070706), 4326),
             'Karnataka', 'Bangalore', '532302',
             'medium', 509581.74,
             'fraud_graph',
             NOW() - interval '274 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '02b443cd-c466-4279-a1f2-8e4570bbb340', 'ficn_seizure',
             'Ficn Seizure reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.420465, 17.388602), 4326),
             'Telangana', 'Hyderabad', '485106',
             'medium', 1268056.75,
             'note_verify',
             NOW() - interval '325 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '6e5a7b91-9e9a-4172-baf7-3961f38201f2', 'phishing',
             'Phishing reported in Delhi',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.193365, 28.703243), 4326),
             'Delhi', 'Delhi', '498320',
             'medium', 1149733.79,
             'citizen_shield',
             NOW() - interval '185 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '59bf1f61-bdf5-4cb4-a05b-c6eb1abc1241', 'other',
             'Other reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.429418, 17.3895), 4326),
             'Telangana', 'Hyderabad', '474575',
             'low', 895665.43,
             'fraud_graph',
             NOW() - interval '155 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '457eef11-da52-405d-8e43-2716c409f5c9', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.815113, 19.27407), 4326),
             'Maharashtra', 'Mumbai', '580805',
             'low', 1234394.50,
             'fraud_graph',
             NOW() - interval '49 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '0d96633d-e2c9-4837-a98a-6349028451a3', 'ficn_seizure',
             'Ficn Seizure reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.799066, 19.035149), 4326),
             'Maharashtra', 'Mumbai', '465498',
             'high', 353326.25,
             'citizen_shield',
             NOW() - interval '48 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '98e86590-e45c-4504-b6d8-a40ad0ce09d5', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.543487, 12.992266), 4326),
             'Karnataka', 'Bangalore', '526493',
             'high', 263489.22,
             'scam_sentinel',
             NOW() - interval '305 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a3a6ad57-d2f5-4f83-ae08-655d044ccae6', 'investment_scam',
             'Investment Scam reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.661668, 12.859343), 4326),
             'Karnataka', 'Bangalore', '414659',
             'low', 1383197.89,
             'citizen_shield',
             NOW() - interval '179 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'b69cb986-b477-485f-b0c1-cd2ae3bfe878', 'digital_arrest',
             'Digital Arrest reported in Hyderabad',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(78.536049, 17.386861), 4326),
             'Telangana', 'Hyderabad', '459432',
             'high', 1122779.59,
             'scam_sentinel',
             NOW() - interval '325 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '7b3138d1-85a4-44d7-98e0-e9f9f7866c32', 'digital_arrest',
             'Digital Arrest reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.560957, 12.945622), 4326),
             'Karnataka', 'Bangalore', '548088',
             'medium', 228622.13,
             'fraud_graph',
             NOW() - interval '79 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '5c091b4f-f933-4043-81b2-447abb126606', 'investment_scam',
             'Investment Scam reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.852505, 19.178), 4326),
             'Maharashtra', 'Mumbai', '550799',
             'high', 759570.37,
             'fraud_graph',
             NOW() - interval '222 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '14ead7cb-a3cc-4bad-8640-94b399e185b1', 'digital_arrest',
             'Digital Arrest reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.79776, 19.049843), 4326),
             'Maharashtra', 'Mumbai', '595379',
             'medium', 78720.09,
             'note_verify',
             NOW() - interval '135 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             'a6b9670f-7d2b-4096-ab73-779fdf242cd8', 'upi_fraud',
             'Upi Fraud reported in Mumbai',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(72.932503, 19.090693), 4326),
             'Maharashtra', 'Mumbai', '526070',
             'high', 841147.79,
             'note_verify',
             NOW() - interval '203 days'
            );
INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '722ddfb3-1489-4d4e-9f9f-5864729b8b9d', 'other',
             'Other reported in Bangalore',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint(77.623199, 12.899025), 4326),
             'Karnataka', 'Bangalore', '463521',
             'medium', 112107.75,
             'note_verify',
             NOW() - interval '166 days'
            );

-- qr_scans.scan_results (flagged)
INSERT INTO qr_scans.scan_results
            (id, user_id, qr_content, content_type, destination_account, risk_level,
             risk_score, complaint_count, explanation, flags)
            VALUES (
             '0ab63e24-6185-4702-b519-9d2873d733c5', (SELECT id FROM core.users WHERE email = 'sumanth@primer.demo'), 'upi://pay?pa=3473979489@okaxis&am=1&cu=INR', 'upi_payment',
             '3473979489@okaxis', 'dangerous', 96, 29,
             'This UPI ID is linked to multiple fraud complaints and appears in the fraud graph as a known mule account.',
             '["linked_to_fraud_account", "high_complaint_count", "recently_created"]'::jsonb
            );
INSERT INTO qr_scans.scan_results
            (id, user_id, qr_content, content_type, destination_account, risk_level,
             risk_score, complaint_count, explanation, flags)
            VALUES (
             'fb98522f-f8cc-4f8a-8bf7-7c70f569fc9e', (SELECT id FROM core.users WHERE email = 'sumanth@primer.demo'), 'upi://pay?pa=7114060331@okhdfcbank&am=1&cu=INR', 'upi_payment',
             '7114060331@okhdfcbank', 'dangerous', 81, 23,
             'This UPI ID is linked to multiple fraud complaints and appears in the fraud graph as a known mule account.',
             '["linked_to_fraud_account", "high_complaint_count", "recently_created"]'::jsonb
            );
INSERT INTO qr_scans.scan_results
            (id, user_id, qr_content, content_type, destination_account, risk_level,
             risk_score, complaint_count, explanation, flags)
            VALUES (
             '7a649ee7-da8d-4583-90a6-8ce910518e95', (SELECT id FROM core.users WHERE email = 'sumanth@primer.demo'), 'upi://pay?pa=3814963909@okhdfcbank&am=1&cu=INR', 'upi_payment',
             '3814963909@okhdfcbank', 'dangerous', 80, 25,
             'This UPI ID is linked to multiple fraud complaints and appears in the fraud graph as a known mule account.',
             '["linked_to_fraud_account", "high_complaint_count", "recently_created"]'::jsonb
            );
INSERT INTO qr_scans.scan_results
            (id, user_id, qr_content, content_type, destination_account, risk_level,
             risk_score, complaint_count, explanation, flags)
            VALUES (
             '5c9af92c-648b-45fc-8f5d-37c5e46ed80c', (SELECT id FROM core.users WHERE email = 'sumanth@primer.demo'), 'upi://pay?pa=5921252890@okaxis&am=1&cu=INR', 'upi_payment',
             '5921252890@okaxis', 'dangerous', 82, 15,
             'This UPI ID is linked to multiple fraud complaints and appears in the fraud graph as a known mule account.',
             '["linked_to_fraud_account", "high_complaint_count", "recently_created"]'::jsonb
            );
INSERT INTO qr_scans.scan_results
            (id, user_id, qr_content, content_type, destination_account, risk_level,
             risk_score, complaint_count, explanation, flags)
            VALUES (
             'f144c43e-b751-436e-a354-28864ba66406', (SELECT id FROM core.users WHERE email = 'sumanth@primer.demo'), 'upi://pay?pa=8238562767@oksbi&am=1&cu=INR', 'upi_payment',
             '8238562767@oksbi', 'dangerous', 99, 8,
             'This UPI ID is linked to multiple fraud complaints and appears in the fraud graph as a known mule account.',
             '["linked_to_fraud_account", "high_complaint_count", "recently_created"]'::jsonb
            );
INSERT INTO qr_scans.scan_results
            (id, user_id, qr_content, content_type, destination_account, risk_level,
             risk_score, complaint_count, explanation, flags)
            VALUES (
             'dbba6aef-f48f-4478-9292-3b4bdd82f3ae', (SELECT id FROM core.users WHERE email = 'sumanth@primer.demo'), 'upi://pay?pa=1234238999@paytm&am=1&cu=INR', 'upi_payment',
             '1234238999@paytm', 'dangerous', 79, 21,
             'This UPI ID is linked to multiple fraud complaints and appears in the fraud graph as a known mule account.',
             '["linked_to_fraud_account", "high_complaint_count", "recently_created"]'::jsonb
            );
INSERT INTO qr_scans.scan_results
            (id, user_id, qr_content, content_type, destination_account, risk_level,
             risk_score, complaint_count, explanation, flags)
            VALUES (
             '068b6dcb-cd39-4a8a-ab0a-f77afa8d50c6', (SELECT id FROM core.users WHERE email = 'sumanth@primer.demo'), 'upi://pay?pa=5353951329@okaxis&am=1&cu=INR', 'upi_payment',
             '5353951329@okaxis', 'dangerous', 84, 31,
             'This UPI ID is linked to multiple fraud complaints and appears in the fraud graph as a known mule account.',
             '["linked_to_fraud_account", "high_complaint_count", "recently_created"]'::jsonb
            );

-- core.investigations + core.case_summaries
INSERT INTO core.investigations
            (id, title, description, type, priority, status, assigned_to, estimated_amount,
             victim_count, tags, created_by)
            VALUES (
             'fc8fdd79-6786-4ea2-9e29-9ffa341b2c07', 'Digital Arrest Fraud Ring — Andheri Cluster', 'Multi-victim digital arrest scam impersonating CBI officials, funds routed through 3 mule accounts before consolidation into a single UPI wallet.', 'digital_arrest', 'critical',
             'active', (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), 625114.63,
             18, '{"digital_arrest","seed_demo"}', (SELECT id FROM core.users WHERE email = 'yashi@primer.demo')
            );
INSERT INTO core.case_summaries
            (id, investigation_id, summary_text, timeline_json, suspects_json, related_complaints,
             confidence_score, source_evidence, generated_by)
            VALUES (
             'f1f3b206-9519-4cb5-a70b-ee1bf14cc23d', 'fc8fdd79-6786-4ea2-9e29-9ffa341b2c07',
             'Multi-victim digital arrest scam impersonating CBI officials, funds routed through 3 mule accounts before consolidation into a single UPI wallet. Cross-referenced against the fraud graph and geo-intel modules, '
             'this case shows a consistent operational pattern with escalating victim counts over '
             'the last quarter.',
             '[{"stage": "first_complaint_filed", "days_ago": 83}, {"stage": "pattern_identified", "days_ago": 47}, {"stage": "fraud_graph_cluster_confirmed", "days_ago": 16}, {"stage": "investigation_opened", "days_ago": 4}]'::jsonb, '[{"role": "call_operator", "status": "unidentified"}, {"role": "mule_account_holder", "status": "identified", "risk": "high"}]'::jsonb, '["NCRP-672967", "NCRP-648684", "NCRP-886804"]'::jsonb,
             76.47, '{"call_recording","cdr_log","fraud_graph_cluster"}',
             'gemini'
            );
INSERT INTO core.investigations
            (id, title, description, type, priority, status, assigned_to, estimated_amount,
             victim_count, tags, created_by)
            VALUES (
             'f5703faf-a50d-485d-a233-580b8339061b', 'CBI Impersonation Network — South Delhi', 'Coordinated CBI impersonation scam targeting retired government employees, using spoofed caller IDs matching real CBI office numbers.', 'cbi_impersonation', 'high',
             'active', (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), 3926730.96,
             14, '{"cbi_impersonation","seed_demo"}', (SELECT id FROM core.users WHERE email = 'yashi@primer.demo')
            );
INSERT INTO core.case_summaries
            (id, investigation_id, summary_text, timeline_json, suspects_json, related_complaints,
             confidence_score, source_evidence, generated_by)
            VALUES (
             'cf7ff057-1675-48f6-b8fe-1ae7d8060f54', 'f5703faf-a50d-485d-a233-580b8339061b',
             'Coordinated CBI impersonation scam targeting retired government employees, using spoofed caller IDs matching real CBI office numbers. Cross-referenced against the fraud graph and geo-intel modules, '
             'this case shows a consistent operational pattern with escalating victim counts over '
             'the last quarter.',
             '[{"stage": "first_complaint_filed", "days_ago": 82}, {"stage": "pattern_identified", "days_ago": 52}, {"stage": "fraud_graph_cluster_confirmed", "days_ago": 10}, {"stage": "investigation_opened", "days_ago": 7}]'::jsonb, '[{"role": "call_operator", "status": "unidentified"}, {"role": "mule_account_holder", "status": "identified", "risk": "high"}]'::jsonb, '["NCRP-711324", "NCRP-795759", "NCRP-652388"]'::jsonb,
             71.09, '{"call_recording","cdr_log","fraud_graph_cluster"}',
             'gemini'
            );
INSERT INTO core.investigations
            (id, title, description, type, priority, status, assigned_to, estimated_amount,
             victim_count, tags, created_by)
            VALUES (
             '46847701-a84b-4a5e-82f8-8e772980a201', 'Customs Seizure Scam — Hyderabad Courier Ring', 'Courier/customs seizure scam operating from call centre with links to 40+ victim complaints across Telangana and Andhra Pradesh.', 'customs_seizure', 'medium',
             'open', (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), 830605.27,
             17, '{"customs_seizure","seed_demo"}', (SELECT id FROM core.users WHERE email = 'yashi@primer.demo')
            );
INSERT INTO core.case_summaries
            (id, investigation_id, summary_text, timeline_json, suspects_json, related_complaints,
             confidence_score, source_evidence, generated_by)
            VALUES (
             'ca98fede-9251-4268-a62d-85a486921e1b', '46847701-a84b-4a5e-82f8-8e772980a201',
             'Courier/customs seizure scam operating from call centre with links to 40+ victim complaints across Telangana and Andhra Pradesh. Cross-referenced against the fraud graph and geo-intel modules, '
             'this case shows a consistent operational pattern with escalating victim counts over '
             'the last quarter.',
             '[{"stage": "first_complaint_filed", "days_ago": 85}, {"stage": "pattern_identified", "days_ago": 52}, {"stage": "fraud_graph_cluster_confirmed", "days_ago": 29}, {"stage": "investigation_opened", "days_ago": 5}]'::jsonb, '[{"role": "call_operator", "status": "unidentified"}, {"role": "mule_account_holder", "status": "identified", "risk": "high"}]'::jsonb, '["NCRP-155663", "NCRP-587546", "NCRP-786563"]'::jsonb,
             93.63, '{"call_recording","cdr_log","fraud_graph_cluster"}',
             'gemini'
            );

-- knowledge_base.patterns
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             'c0530ced-8a6a-47ab-b1ff-918080b6fd84', 'Digital Arrest Impersonation', 'Scammer poses as CBI/police/customs official claiming the victim is under ''digital arrest'' and must stay on video/voice call while transferring funds to ''safe government accounts''.', 'digital_arrest', 'en',
             '{"stay on call","safe custody account","aadhaar linked parcel","video call surveillance"}', '{"Scammer poses as CBI/police/customs official claiming the victim is under ''digit"}',
             39, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             'f2cd012d-76b5-4e76-ada2-937b6d12645f', 'CBI/Police FIR Threat', 'Caller claims an FIR or non-bailable warrant exists against the victim and demands urgent bank verification or payment to ''settle'' the case.', 'cbi_impersonation', 'en',
             '{"FIR registered","non-bailable warrant","urgent verification"}', '{"Caller claims an FIR or non-bailable warrant exists against the victim and deman"}',
             203, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             'c602d04d-ea6b-43e0-9d5c-e545f537dbb1', 'Customs/Courier Parcel Seizure', 'Caller claims a parcel in the victim''s name was seized at customs containing contraband, and demands a penalty payment to avoid prosecution.', 'customs_seizure', 'en',
             '{"parcel seized","contraband found","customs penalty"}', '{"Caller claims a parcel in the victim''s name was seized at customs containing con"}',
             143, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             '6d23904d-8242-4d7c-b806-5ddffbc4d7ad', 'Fake Income Tax Notice', 'Caller impersonates Income Tax officials citing discrepancies in filings and pressures the victim to pay ''pending dues'' immediately via UPI.', 'tax_evasion', 'en',
             '{"tax discrepancy","pending dues","pay via UPI"}', '{"Caller impersonates Income Tax officials citing discrepancies in filings and pre"}',
             189, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             '69f1589c-1be0-4a44-8629-1eab172e1665', 'KYC Expiry / Account Block', 'SMS or call claims the victim''s bank/UPI KYC will expire, requesting OTP or personal banking details to ''reactivate'' the account.', 'bank_kyc', 'en',
             '{"KYC expiry","share OTP","reactivate account"}', '{"SMS or call claims the victim''s bank/UPI KYC will expire, requesting OTP or pers"}',
             60, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             '51455fe1-be12-4c97-8d1d-cacf61496e02', 'Investment / Trading App Scam', 'Victim is lured into a fake trading app showing inflated returns, then blocked from withdrawing after depositing larger sums.', 'investment_scam', 'en',
             '{"guaranteed returns","fake trading app","withdrawal blocked"}', '{"Victim is lured into a fake trading app showing inflated returns, then blocked f"}',
             14, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             'fb5d13f5-a3c6-4bab-b2ca-2fdcf2cbf55f', 'Loan App Harassment', 'Predatory loan apps extract contacts/photos during KYC then use them to harass and blackmail borrowers into paying inflated amounts.', 'loan_fraud', 'en',
             '{"instant loan approval","contact list access","harassment for repayment"}', '{"Predatory loan apps extract contacts/photos during KYC then use them to harass a"}',
             154, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             '660e46dd-12b2-45c4-af9c-288ebb6131ff', 'QR Code / UPI Refund Scam', 'Scammer sends a QR code disguised as a ''refund'' request; scanning and entering UPI PIN actually authorizes an outgoing payment.', 'upi_fraud', 'en',
             '{"scan to receive refund","enter UPI PIN to collect","reverse QR trick"}', '{"Scammer sends a QR code disguised as a ''refund'' request; scanning and entering U"}',
             202, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             '24e9af8c-de1d-4c31-b228-ee7b164671c8', 'Job Offer Advance Fee Scam', 'Fake recruiter offers a high-paying remote job and asks for ''registration'' or ''training kit'' fees upfront before disappearing.', 'job_scam', 'en',
             '{"work from home offer","registration fee","training kit payment"}', '{"Fake recruiter offers a high-paying remote job and asks for ''registration'' or ''t"}',
             123, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             '1521391e-e87a-4045-8ccc-82dd289e3ca7', 'Sextortion / Video Call Blackmail', 'Victim is lured into a compromising video call, recorded without consent, then blackmailed with threats to share the recording with contacts.', 'sextortion', 'en',
             '{"compromising video call","recording threat","share with contacts"}', '{"Victim is lured into a compromising video call, recorded without consent, then b"}',
             199, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );
INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             '95f07c55-50bd-456a-a9cd-b9fb8ecc7c87', 'Electricity Bill Disconnection Scam', 'SMS/call claims electricity connection will be disconnected tonight over unpaid dues, urging the victim to install a remote-access app to ''pay directly''.', 'utility_scam', 'en',
             '{"bill disconnection tonight","install remote app","pay directly"}', '{"SMS/call claims electricity connection will be disconnected tonight over unpaid "}',
             265, (SELECT id FROM core.users WHERE email = 'yashi@primer.demo'), TRUE
            );

COMMIT;
