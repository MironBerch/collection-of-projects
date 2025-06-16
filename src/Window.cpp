#include <range/v3/all.hpp>
#include <AUI/View/ARadioButton.h>
#include <AUI/View/ARadioGroup.h>
#include <AUI/Model/AListModel.h>
#include "AUI/ASS/Property/BackgroundSolid.h"
#include "AUI/ASS/Property/Border.h"
#include "AUI/ASS/Property/TransformOffset.h"
#include "AUI/ASS/Selector/on_state.h"
#include "AUI/Layout/AVerticalLayout.h"
#include "AUI/Model/ATreeModel.h"
#include "AUI/View/A2FingerTransformArea.h"
#include "AUI/View/AButton.h"
#include "AUI/Layout/AHorizontalLayout.h"
#include "AUI/Platform/ACustomCaptionWindow.h"
#include "AUI/View/ACircleProgressBar.h"
#include "AUI/View/ALabel.h"
#include "AUI/Layout/AStackedLayout.h"
#include "AUI/View/ATextField.h"
#include "AUI/View/ASpacerExpanding.h"
#include "AUI/Util/UIBuildingHelpers.h"
#include "AUI/View/ASpinnerV2.h"
#include "AUI/View/AGroupBox.h"
#include "AUI/Util/ALayoutInflater.h"
#include "AUI/View/ASlider.h"
#include "AUI/Platform/APlatform.h"
#include "AUI/IO/AByteBufferInputStream.h"
#include "AUI/View/ASpinnerV2.h"
#include <AUI/i18n/AI18n.h>
#include <AUI/i18n/AI18n.h>
#include <AUI/ASS/ASS.h>
#include <AUI/View/ATextArea.h>
#include <AUI/View/ARulerView.h>
#include <AUI/View/AForEachUI.h>
#include <AUI/View/ARulerArea.h>
#include <AUI/Platform/ADesktop.h>
#include <AUI/Platform/AMessageBox.h>
#include <AUI/View/ASplitter.h>
#include <AUI/View/AScrollArea.h>
#include <AUI/View/ATabView.h>
#include <AUI/View/AGridSplitter.h>
#include <AUI/View/AText.h>
#include <AUI/View/ADrawableView.h>
#include <AUI/Traits/platform.h>

#include <memory>
#include <random>

#include "Window.h"

using namespace declarative;

void fillWindow(_<AViewContainer> t) {
    t->setLayout(std::make_unique<AStackedLayout>());
    t->addView(_new<ALabel>("Window contents"));
}

ExampleWindow::ExampleWindow() : AWindow("Examples", 800_dp, 700_dp) {
    allowDragNDrop();

    setLayout(std::make_unique<AVerticalLayout>());
    AStylesheet::global().addRules({ {
      c(".all_views_wrap") > t<AViewContainer>(),
      Padding { 16_dp },
    } });

    _<ATabView> tabView;
    _<AProgressBar> progressBar = _new<AProgressBar>();
    _<ACircleProgressBar> circleProgressBar = _new<ACircleProgressBar>();

    addView(tabView = _new<ATabView>() let {
        it->addTab(
            AScrollArea::Builder().withContents(std::conditional_t<
                                                aui::platform::current::is_mobile(), Vertical, Horizontal> {
              Vertical {
                // buttons
                GroupBox {
                  Label { "Buttons" },
                  Vertical {
                    _new<AButton>("Common button"),
                  },
                },

                GroupBox {
                  Label { "System dialog" },
                  Vertical {
                    _new<AButton>("Show file chooser")
                        .connect(&AView::clicked, this,
                                 [&] {
                                     mAsync << ADesktop::browseForFile(this).onSuccess([&](const APath& f) {
                                         if (f.empty()) {
                                             AMessageBox::show(this, "Result", "Cancelled");
                                         } else {
                                             AMessageBox::show(this, "Result", "File: {}"_format(f));
                                         }
                                     });
                                 }),
                    _new<AButton>("Show folder chooser")
                        .connect(&AView::clicked, this,
                                 [&] {
                                     mAsync << ADesktop::browseForDir(this).onSuccess([&](const APath& f) {
                                         if (f.empty()) {
                                             AMessageBox::show(this, "Result", "Cancelled");
                                         } else {
                                             AMessageBox::show(this, "Result", "Folder: {}"_format(f));
                                         }
                                     });
                                 }),
                    _new<AButton>("Message box")
                        .connect(&AView::clicked, this,
                                 [&] {
                                     /// [AMessageBox]
                                     AMessageBox::show(this,
                                                       "Title",
                                                       "Message",
                                                       AMessageBox::Icon::NONE,
                                                       AMessageBox::Button::OK);
                                     /// [AMessageBox]
                                 }),
                    _new<AButton>("Cause assertion fail")
                        .connect(&AView::clicked, this, [&] { AUI_ASSERT_NO_CONDITION("assertion fail"); }),
                  },
                },
              },
              Vertical::Expanding {
                // fields

                GroupBox {
                  Label { "Fields" },
                  Vertical::Expanding {
                    Label { "Text area" },
                    AScrollArea::Builder()
                            .withContents(_new<ATextArea>(
                                "AUI Framework - Declarative UI toolkit for modern C++20\n"
                                "Copyright (C) 2020-2025 Alex2772 and Contributors\n"
                                "\n"
                                "SPDX-License-Identifier: MPL-2.0\n"
                                "\n"
                                "This Source Code Form is subject to the terms of the Mozilla "
                                "Public License, v. 2.0. If a copy of the MPL was not distributed with this "
                                "file, You can obtain one at http://mozilla.org/MPL/2.0/."))
                            .build()
                        << ".input-field" let { it->setExpanding(); },
                  } }
    with_style { Expanding {} } } }),
            "Common");


        //             Vertical::Expanding {
        //               _new<ALabel>("Default"),
        //               AText::fromString(
        //                   "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
        //                   "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
        //                 ) with_style { ATextAlign::JUSTIFY },
        //             } with_style { MinSize { 200_dp } },
        //             Vertical::Expanding {
        //               _new<ALabel>("Word breaking"),
        //               AText::fromString(
        //                   "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
        //                   "proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
        //                   { WordBreak::BREAK_ALL }),
        //             } with_style { MinSize { 200_dp } },

        //           [] {
        //               _<AViewContainer> v1 = Vertical {};
        //               _<AViewContainer> v2 = Vertical {};
        //               for (int i = 0; i <= 9; ++i) {
        //                   v1->addView(Horizontal {
        //                     _new<ALabel>("{} px"_format(i + 6)),
        //                     _new<ALabel>("Hello! [] .~123`") with_style { FontSize { AMetric(i + 6, AMetric::T_PX) } } });
        //                   v2->addView(Horizontal {
        //                     _new<ALabel>("{} px"_format(i + 16)),
        //                     _new<ALabel>("Hello! [] .~123`") with_style { FontSize { AMetric(i + 16, AMetric::T_PX) } } });
        //               }
        //               return Horizontal { v1, v2 };

        it->setExpanding();
    });

    addView(Horizontal {
      _new<ASpacerExpanding>(),
      _new<ALabel>("\u00a9 Alex2772, 2021, alex2772.ru") let {
              it << "#copyright";
              it->setEnabled(false);
          },
    });
}
